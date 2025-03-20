#!/bin/bash

base_dir=$(dirname "$full_path")
cd "$base_dir"

# docker ps | grep nextcloud-1
docker exec -it $(docker ps --filter "name=docker-web-unstructured_unstructured_1" --format "{{.ID}}") bash
