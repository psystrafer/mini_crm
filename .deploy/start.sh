#!/bin/bash


### apply migrations
alembic upgrade head


### start
fastapi run --port 8000 src/main.py