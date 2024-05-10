#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/tictactoe.py",target=/app/tictactoe.py -it --env-file env cs-ai