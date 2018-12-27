from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_DIR = f'{BASE_DIR}/job_search/repository/database'
    SQLALCHEMY_DATABASE_URI = f'{SQLALCHEMY_DATABASE_DIR}/app.db'
    SQLITE_DATABASE_URI = f'sqlite:///{SQLALCHEMY_DATABASE_DIR}/app.db'
