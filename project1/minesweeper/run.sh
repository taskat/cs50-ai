#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/minesweeper.py",target=/app/minesweeper.py -it $@ cs-ai