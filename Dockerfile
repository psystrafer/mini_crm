FROM python:3.13

WORKDIR /app

COPY . .

RUN pip install poetry &&  \
    poetry config virtualenvs.create false &&  \
    poetry install --no-root

RUN chmod +x .deploy/start.sh

ENTRYPOINT /app/.deploy/start.sh
