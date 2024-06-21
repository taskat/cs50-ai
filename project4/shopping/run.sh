#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/shopping.py",target=/app/shopping.py --mount type=bind,source="$PWD/requirements.txt",target=/app/requirements.txt -it -e FILE=shopping.py -e PROJECT=shopping $@ cs-ai