#!/bin/bash
pip install -r /app/requirements.txt
style50 $FILE
check50 --local ai50/projects/2024/x/$PROJECT
if [ -v SUBMIT ]; then
    submit50 ai50/projects/2024/x/$PROJECT
fi