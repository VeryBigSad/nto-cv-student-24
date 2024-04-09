#!/bin/bash

# echo "Waiting for postgres database"
# while ! $(nc -z postgres 5432) ; do
#   sleep 0.1
# done;
# echo "Postgres database - started"
# sleep 1

uvicorn main:app --host  0.0.0.0 --port 80