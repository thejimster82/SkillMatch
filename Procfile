release: python manage.py migrate && python manage.py get_courses
web: gunicorn skillmatch.wsgi:application --log-file -