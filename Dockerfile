FROM python:3.11-slim

WORKDIR /app

# System deps for lxml / pillow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default: Streamlit web UI
EXPOSE 8501
CMD ["streamlit", "run", "webapp.py", "--server.address=0.0.0.0", "--server.port=8501"]
