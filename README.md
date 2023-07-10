# FastAPI

A blog API that handles basic CRUD operations on users, posts, and likes.

### Built with:
- Python
- [FastAPI](https://fastapi.tiangolo.com/)
- [PostgreSQL](https://www.postgresql.org)
- [Swagger](https://swagger.io/)
- [Postman](https://www.postman.com/)

### Installation
Install with pip:
```
$ pip install -r requirements.txt
```

### Environment Configurations
Create a `.env` file with these configurations:
```
DATABASE_HOSTNAME=...
DATABASE_PORT=...
DATABASE_PASSWORD=...
DATABASE_NAME=...
DATABASE_USERNAME=...
SECRET_KEY=...
ALGORITHM=...
ACCESS_TOKEN_EXPIRES_MINUTES=...
```

### Run
```
uvicorn app.main:app --reload
```
Default port is http://127.0.0.1:8000
