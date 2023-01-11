ARG PYTHON_VERSION=latest
FROM python:${PYTHON_VERSION} as python

FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

RUN apt update --fix-missing && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY tradesocket.txt ./
RUN pip wheel --wheel-dir /usr/src/trade_socket/wheels  \
    -r tradesocket.txt

FROM python as python-run-stage

EXPOSE 8080-8099:8080-8099
ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/trade_socket

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt update --fix-missing && apt-get install --no-install-recommends -y \
    libpq-dev \
    gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/trade_socket/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY . ${APP_HOME}

COPY ./entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

# CMD [ "python3", "/trade_socket/hectperconnbind.py" ]
