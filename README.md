# FastAPI with Alembic and OAuth2

## Overview

This project is a FastAPI application

# Instalation

1. Clone the repository

```bash
git clone https://github.com/Bonker009/poseidon.git
```

2. Change the project repo

```bash
cd poseidon
```

3. Create virtual enviroments

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

4. Install Dependencies

```bash
pip install -r requirements.txt
```

5. Set up database

```bash
DATABASE_URL="postgresql://username:password@localhost:5432/db_name"
```

6. Crate first migration

```bash
alembic revision --autogenerate -m "new migration"
```

7. Apply migration

```bash
alembic upgrade head
```

# Ruuning The Application

```bash
uvicorn main:app --reload
```

or

```bash
fastapi dev main.py
```

## Usage

- Navigate to <a href="http://127.0.0.1:8000/docs">http://127.0.0.1:8000/docs</a> to access the interactive API documentation.
- Navigate to <a href="http://127.0.0.1:8000/redocs">http://127.0.0.1:8000/docs</a>` to access the ReDoc interactive API documentation.
- Navigate to <a href="http://127.0.0.1:8000">http://127.0.0.1:8000/docs</a> for additional information or to view the API.

# Commands

- Create a new migration: alembic revision --autogenerate -m "Migration message"
- Apply migrations: alembic upgrade head
- Rollback the last migration: alembic downgrade -1
