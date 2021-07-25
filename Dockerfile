# syntax=docker/dockerfile:experimental
FROM python:3.8.1 as intermediate

ENV PYTHONUNBUFFERED=1

COPY ./doc/requirements/ /requirements

RUN --mount=type=ssh pip install --no-cache-dir -r /requirements/base.txt

COPY ./entrypoint /entrypoint

RUN chmod -R +x /entrypoint

WORKDIR /app

ENTRYPOINT ["/entrypoint/entrypoint.sh"]
