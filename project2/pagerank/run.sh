#!/bin/bash
PWD = $(pwd)
docker run --name cs-ai --rm --mount type=bind,source="$PWD/pagerank.py",target=/app/pagerank.py -it -e FILE=pagerank.py -e PROJECT=pagerank $@ cs-ai