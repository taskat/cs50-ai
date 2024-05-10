#!/bin/bash
style50 minesweeper.py
check50 --local ai50/projects/2024/x/minesweeper
if [ -v SUBMIT ]; then
    submit50 ai50/projects/2024/x/minesweeper
fi