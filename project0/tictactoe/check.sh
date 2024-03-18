#!/bin/bash
style50 tictactoe.py
check50 --local ai50/projects/2024/x/tictactoe

if [ "$SUBMIT" = "true" ]; then
    submit50 ai50/projects/2024/x/tictactoe
fi