# ---------- build stage: JS bundle + Python backend codegen ----------
FROM node:22-slim AS builder

RUN apt-get update && \
    apt-get install -y --no-install-recommends python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY src/ src/
COPY .babelrc webpack.config.js ./
COPY dash_loading_components/ dash_loading_components/

ENV REACT_VERSION=19.2.4
RUN npm run build:js

RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir "dash[dev]>=4.5.0rc0"

RUN /opt/venv/bin/dash-generate-components \
    ./src/lib/components dash_loading_components \
    -p package-info.json --r-prefix '' --jl-prefix '' --ignore '\.test\.'

# ---------- runtime stage: slim Python image ----------
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    REACT_VERSION=19.2.4

WORKDIR /app

COPY requirements-gallery.txt ./
RUN pip install --no-cache-dir -r requirements-gallery.txt

COPY setup.py package.json README.md LICENSE MANIFEST.in ./
COPY --from=builder /app/dash_loading_components/ dash_loading_components/
RUN pip install --no-cache-dir .

COPY gallery.py ./
COPY assets/ assets/

EXPOSE 8050

# A production WSGI server, not Flask's development server. Render sets PORT.
# One worker per core is plenty for a gallery; threads cover concurrent
# callbacks. --preload imports the app once so workers share its memory.
CMD ["sh", "-c", "exec gunicorn gallery:server --bind 0.0.0.0:${PORT:-8050} --workers 2 --threads 4 --preload --access-logfile -"]
