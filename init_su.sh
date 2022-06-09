#!/bin/sh

echo "------ create default admin user ------"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('201710911', 'admin@myapp.local', 'roal@!3578')" | python manage.py shell
