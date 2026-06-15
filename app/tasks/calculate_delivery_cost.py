import asyncio
from decimal import Decimal

import structlog

from app.db.session import get_session_ctx
from app.integration.cbr import CbrRateFetchError, get_usd_rate
from app.repositories.package import PackageDAL
from app.tasks.celery_app import celery_app

logger = structlog.get_logger(__name__)

WEIGHT_FEE = Decimal("0.5")
VALUE_FEE = Decimal("0.01")


def _calculate_delivery_cost(weight: Decimal, value_usd: Decimal, rate: Decimal) -> Decimal:
    return (
        weight * WEIGHT_FEE + value_usd * VALUE_FEE
    ) * rate


@celery_app.task
def calculate_delivery_cost():
    structlog.contextvars.clear_contextvars()
    structlog.contextvars.bind_contextvars(task="calculate_delivery_cost")
    try:
        logger.info("delivery_calculation.started")
        asyncio.run(_calculate())
    finally:
        structlog.contextvars.clear_contextvars()


async def _calculate() -> None:
    async with get_session_ctx() as session:
        package_dal = PackageDAL(session)
        packages = await package_dal.get_zero_packages()
        if not packages:
            logger.info("delivery_calculation.skipped", reason="no_packages")
            return

        try:
            rate = Decimal(str(await get_usd_rate()))
        except CbrRateFetchError:
            logger.error("delivery_calculation.rate_unavailable")
            return

        for package in packages:
            package.delivery_cost_rub = _calculate_delivery_cost(
                Decimal(str(package.weight)),
                Decimal(str(package.value_usd)),
                rate,
            ).quantize(Decimal("0.01"))

        logger.info(
            "delivery_calculation.completed",
            packages_count=len(packages),
            usd_rate=str(rate),
        )
