#!/bin/env bash

# scriptn to setup django
# run script:
# 	chmod +x dj_run.sh
# 	./dj_run.sh


# create a virtual environment if it doesn't exist
# if [ ! -d "../.dj_sim" ]; then
#    python3 -m virtualenv ../.dj_sim
# fi

# activate the virtual environment
. ../.dj_sim/bin/activate

# dependencies from requirements.txt
# if [ -f "requirements.txt" ]; then
  #  pip install -r requirements.txt
#fi

# python manage.py migrate

# collect static files - if deploying)
# python manage.py collectstatic --noinput

python manage.py runserver

