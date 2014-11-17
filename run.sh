#!/usr/bin/env sh
gunicorn app:app -p bookclub.pid -b 127.0.0.1:5001 -D
