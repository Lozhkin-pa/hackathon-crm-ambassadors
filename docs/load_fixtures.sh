#!/bin/bash

python ../manage.py loaddata ../ambassadors/fixtures/ambassador_goal_fixture.json
python ../manage.py loaddata ../ambassadors/fixtures/course_fixture.json
python ../manage.py loaddata ../ambassadors/fixtures/education_goal_fixture.json
python ../manage.py loaddata ../ambassadors/fixtures/ambassadors_fixture.json
python ../manage.py loaddata ../ambassadors/fixtures/promo_fixture.json
python ../manage.py loaddata ../users/fixtures/user_fixture.json
python ../manage.py loaddata ../merch/fixtures/merch_fixture.json
python ../manage.py loaddata ../ambassadors/fixtures/merchmiddle_fixture.json
python ../manage.py loaddata ../content/fixtures/content_fixture.json


