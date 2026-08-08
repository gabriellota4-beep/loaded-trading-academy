release: python manage.py migrate --noinput && python manage.py seed_courses
web: gunicorn loaded_academy.wsgi
