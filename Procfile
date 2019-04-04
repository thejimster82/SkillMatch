release: python manage.py migrate && python ./matching/services.py update_courses
web: gunicorn skillmatch.wsgi:application --log-file -