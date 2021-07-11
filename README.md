# url-shortener

## Usage
1. Create and fill `.env` file in `docker/dev/` directory
2. Build docker image
```bash
$ docker-compose up --build -d
```
3. Migrate and createsuperuser
```bash
$ docker exec -ti django sh
$ python manage.py migrate
$ python manage.py createsuperuser
```
