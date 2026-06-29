FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    python -m playwright install chromium && \
    playwright install-deps chromium

# Copy source code
COPY . .

# Run bot
CMD ["python3", "bot_pmi.py"]
