FROM python:3.11-slim

RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc libffi-dev musl-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/entrypoint.sh"]
