#!/bin/sh
prisma generate
prisma migrate dev
#python seed.py
python -u -m flask run --host=0.0.0.0 --port=5000 