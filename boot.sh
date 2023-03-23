#!/bin/bash
source venv/bin/activate
gunicorn -b :5000 -w 4 'proscons:create_app()' --access-logfile - --error-logfile -

# partially copied from microblog