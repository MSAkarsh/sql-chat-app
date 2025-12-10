# SQLite + Python (SQLAlchemy) example

This project is a minimal example showing how to use SQLite with SQLAlchemy (ORM).

Quick start:

```bash
cd ~/Downloads/sqlite_sqlalchemy_example
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python3 -m src.create_db
python3 -m src.example_crud
```

Files:
- `src/db.py` — SQLAlchemy engine, session and base
- `src/models.py` — example `User` and `Post` models
- `src/create_db.py` — create the SQLite database and tables
- `src/example_crud.py` — small script demonstrating create/read/update/delete

The SQLite database will be created as `data.db` in the project root. Add it to `.gitignore` if necessary.
