#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/traffic.py",target=/app/traffic.py --mount type=bind,source="$PWD/requirements.txt",target=/app/requirements.txt -it -e FILE=traffic.py -e PROJECT=traffic $@ cs-ai