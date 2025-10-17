FROM python:3.9-slim

LABEL maintainer="OCR Project"
LABEL description="High-Accuracy Chinese-English OCR Document Recognition System"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgomp1 \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

VOLUME ["/app/input", "/app/output"]

ENTRYPOINT ["python", "main.py"]

CMD ["-i", "/app/input", "-o", "/app/output"]
