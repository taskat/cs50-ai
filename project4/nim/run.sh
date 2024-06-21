#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/nim.py",target=/app/nim.py -it -e FILE=nim.py -e PROJECT=nim $@ cs-ai