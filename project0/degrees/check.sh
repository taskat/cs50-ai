#!/bin/bash
style50 degrees.py
style50 util.py
check50 --local ai50/projects/2024/x/degrees

if [ -v SUBMIT ]; then
    submit50 ai50/projects/2024/x/degrees
fi