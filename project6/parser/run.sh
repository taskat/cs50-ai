#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/parser.py",target=/app/parser.py --mount type=bind,source="$PWD/requirements.txt",target=/app/requirements.txt -it -e FILE=parser.py -e PROJECT=parser $@ cs-ai