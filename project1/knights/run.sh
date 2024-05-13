#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/puzzle.py",target=/app/puzzle.py -it -e FILE=puzzle.py -e PROJECT=knights $@ cs-ai