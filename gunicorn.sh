#!/bin/bash
source /etc/environment
source venv/bin/activate

exec gunicorn --workers=3 --threads=3 app:app
