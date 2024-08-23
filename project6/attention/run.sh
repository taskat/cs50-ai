#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/mask.py",target=/app/mask.py --mount type=bind,source="$PWD/requirements.txt",target=/app/requirements.txt -it -e FILE=mask.py -e PROJECT=attention $@ cs-ai