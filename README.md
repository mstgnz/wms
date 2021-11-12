# Worksite-Django
Worksite Management System With Django

## via docker
first step, run the docker service
```
docker-compose -f docker-compose.yml up -d
```

open terminal and list docker services. Enter the container of django-app and run the following commands.

```
python manage.py makemigrations
python manage.py migrate
```

if it is the first installation;
Create a superuser with the `python manage.py createsuperuser`

For each model added later, you have to do the migrate process in the same way.

That's it. Go to url

`http://localhost:8000`


Note : The project is not yet completed and will be completed when I have free time.