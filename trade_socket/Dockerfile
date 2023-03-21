ARG PYTHON_VERSION=3.10-slim-bullseye
FROM myproj_local_django as python

FROM python as python-build-stage
ARG BUILD_ENVIRONMENT=local

COPY ./requirements .
RUN pip wheel --wheel-dir /usr/src/app/wheels  \
    -r tradesocket.txt

FROM python as python-run-stage

EXPOSE 8080-8099:8080-8099
ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./trade_socket/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./trade_socket/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY . ${APP_HOME}
