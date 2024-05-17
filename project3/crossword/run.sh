#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/generate.py",target=/app/generate.py -it -e FILE=generate.py -e PROJECT=crossword $@ cs-ai