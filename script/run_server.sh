#!/usr/bin/env bash

export PYTHONPATH="/server/src/:$PYTHONPATH"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
