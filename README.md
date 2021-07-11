# url-shortener

## Usage
1. Build docker image
```bash
$ docker-compose up --build -d
```
2. Migrate and createsuperuser
```bash
$ docker exec -ti django sh
$ python manage.py migrate
$ python manage.py createsuperuser
```
