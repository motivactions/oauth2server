FROM python:3.8.1-buster as builder
ARG PYTHONUNBUFFERED=1
RUN apt-get update --yes && apt-get install --yes --no-install-recommends \
    build-essential wget gdebi \
    gdal-bin libgdal-dev python3-gdal \
    libproj-dev binutils \
    libpq-dev libmariadb-dev-compat libmariadb-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev libwebp-dev \
    git
COPY requirements.txt /
RUN pip wheel -r /requirements.txt  --wheel-dir /usr/src/app/wheels

FROM python:3.8.1-buster as runner
COPY --from=builder /usr/src/app/wheels  /wheels/
RUN set -ex; \
    pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/*; \
    apt update; apt install -y gdal-bin; \
    rm -rf /wheels/; \
    useradd --shell /bin/false django; \
    mkdir -p /app; \
    chown django:django /app
WORKDIR /app
COPY --chown=django:django . .
COPY ./entrypoint.sh /entrypoint.sh

RUN chmod +x ./entrypoint.sh

ENV PYTHONUNBUFFERED=1 \
    PORT=8000
EXPOSE 8000

USER django
ENTRYPOINT ["./entrypoint.sh"]
CMD ["gunicorn", "server.wsgi:application", "0.0.0.0:8000", "--log-level=DEBUG"]
