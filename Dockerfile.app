FROM python:3.12-slim
WORKDIR /app

# Install system deps for mysql + fonts for reportlab/matplotlib
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libmariadb-dev \
    pkg-config \
    fonts-liberation \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY server.py .
COPY registration/ ./registration/
COPY web/ ./web/
COPY .carol_data/ ./.carol_data/

ENV PYTHONUNBUFFERED=1
ENV DB_HOST=db
ENV DB_PORT=3306
ENV DB_NAME=carol
ENV DB_USER=carol
ENV DB_PASSWORD=carolpass
ENV PORT=8000
ENV HOST=0.0.0.0

EXPOSE 8000

CMD ["python3", "server.py"]
