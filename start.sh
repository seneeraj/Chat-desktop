#!/usr/bin/env bash

cd app
uvicorn main:app --host 0.0.0.0 --port 10000
