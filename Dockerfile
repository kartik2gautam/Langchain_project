FROM python:3.11-slim

WORKDIR /app

# Install minimal system deps (if needed for wheels) and Python deps
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code (put files from repo `app/` into container /app)
COPY app/ .

ENV PYTHONUNBUFFERED=1

# Run uvicorn against the simple `main:app` module (single main file)
CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]