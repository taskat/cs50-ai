#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/heredity.py",target=/app/heredity.py -it -e FILE=heredity.py -e PROJECT=heredity $@ cs-ai