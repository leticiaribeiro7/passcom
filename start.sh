#!/bin/sh
prisma generate
prisma migrate dev --name "init"
python -u -m flask run --host=0.0.0.0 --port=5000 
