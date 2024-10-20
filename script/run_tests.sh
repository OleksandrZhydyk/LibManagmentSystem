#!/usr/bin/env bash

export PYTHONPATH="/server/src/:$PYTHONPATH"
pytest -s --disable-warnings >> /server/logs/tests.log
