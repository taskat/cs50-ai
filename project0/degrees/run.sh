#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/degrees.py",target=/app/degrees.py -it -e FILE=degrees.py -e PROJECT=degrees $@ cs-ai