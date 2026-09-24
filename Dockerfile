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

ENV REACT_VERSION=19.2.4
RUN npm run build:js

RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --no-cache-dir "dash[dev]>=4.5"

COPY dash_loading_components/package-info.json dash_loading_components/package-info.json
COPY dash_loading_components/__init__.py dash_loading_components/__init__.py
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

CMD ["python", "gallery.py"]
