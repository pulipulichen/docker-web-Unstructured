#!/bin/bash

docker-compose down
git pull
docker-compose up --build -d
docker-compose logs -f