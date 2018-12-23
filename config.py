from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_DATABASE_URI = f'{BASE_DIR}/job_search/repository/app.db'
