# URL shortener

- URLs binds to current session id
- No authorization
- Shortened URLs isn't restricted by session id (user with any session id can be redirected via shortened url)

## Usage
1. Create and fill `.env` file in `docker/dev/` directory
2. Build docker image
```bash
$ docker-compose build
```
3. Run docker containers
```bash
$ docker-compose up -d
```
4. Run tests
```bash
$ docker exec -ti django python manage.py test .
```
