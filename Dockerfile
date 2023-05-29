FROM python:3.9-slim-buster
WORKDIR /backend
COPY . /backend
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV DJANGO_SETTINGS_MODULE=kpoOrderProject.settings
EXPOSE 8000
CMD ["bash", "build.sh"]