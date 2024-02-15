#!/bin/bash

rm db.sqlite3
rm -rf ./kingdomdeathapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations kingdomdeathapi
python3 manage.py migrate kingdomdeathapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata players
python3 manage.py loaddata settlements
python3 manage.py loaddata resource_types
python3 manage.py loaddata resources
python3 manage.py loaddata events
python3 manage.py loaddata milestone_types
python3 manage.py loaddata milestones
python3 manage.py loaddata weapon_proficiencies
python3 manage.py loaddata fighting_arts
python3 manage.py loaddata disorders
python3 manage.py loaddata abilities
python3 manage.py loaddata survivors