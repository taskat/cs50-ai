#!/bin/bash
style50 puzzle.py
check50 --local ai50/projects/2024/x/knights

if [ "$SUBMIT" = "true" ]; then
    submit50 ai50/projects/2024/x/knights
fi