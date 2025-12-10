from .db import engine, Base
from . import models


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Database and tables created at 'data.db'")


if __name__ == "__main__":
    init_db()
