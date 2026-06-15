FROM python:3.12-slim
LABEL version="1.0"
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN useradd -m appuser
USER appuser
CMD ["python", "main.py"]