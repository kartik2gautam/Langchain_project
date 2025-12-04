FROM python:3.11-slim

WORKDIR /app

# Install minimal system deps (if needed for wheels) and Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app ./app

ENV PYTHONUNBUFFERED=1

CMD ["python", "app/main.py"]
