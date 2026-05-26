FROM python:3.11-slim

WORKDIR /app

# System deps for GeoPandas / PostGIS
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin libgdal-dev \
    libgeos-dev libproj-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

ENV CPLUS_INCLUDE_PATH=/usr/include/gdal
ENV C_INCLUDE_PATH=/usr/include/gdal

# Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# App
COPY . .

EXPOSE 8050 8888

CMD ["python", "dashboards/app.py"]
