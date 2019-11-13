#!/bin/bash
python3 /src/project/manage.py migrate --no-input
python3 /src/project/manage.py collectstatic --no-input
locale-gen "pt_BR.UTF-8"