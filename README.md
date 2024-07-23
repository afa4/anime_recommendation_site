# Anime Recommendation Site

### required env vars

```
MAL_API_TOKEN=MyAnimeListJWTAccessToken
API_URL=http://host.docker.internal:8080
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
```
### django utils

python shell in django context:

```shell
python manage.py shell
```

run django server:

```shell
python manage.py runserver
```

