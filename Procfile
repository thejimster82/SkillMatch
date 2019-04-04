release: python manage.py migrate && python manage.py update_courses
web: gunicorn skillmatch.wsgi:application --log-file -