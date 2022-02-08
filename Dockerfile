FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app/
WORKDIR /app/

COPY . .


RUN \
    apt-get update && \
    apt-get install -y libpq-dev gcc postgresql-client && \
    python -m pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["/bin/bash","/app/api_entrypoint.sh"]
