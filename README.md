#  Project "University"

###  About project:

University manager.

### Technology stack
```
Python 3
Django
Django REST Framework
PostgreSQL
Docker
Celery
Redis
Pandas
```

## How to start a project:
 
1. Download a project
2. Install docker, docker-compose
3. Create .env with these constants (use .env.example)
4. Building and running a container
```
docker-compose up -d --build
```
5. Apply migrations
```
docker-compose exec -it container_id bash python3 manage.py migrate
```

6. Creating a superuser
```
docker-compose exec -it container_id bash python3 manage.py createsuperuser
```

## API documentation:

Documentation implemented through auto-generation

Swagger documentation (core)
```
http://localhost/swagger-core/
```
ReDoc documentation (core)
```
http://localhost/redoc-core/
```
