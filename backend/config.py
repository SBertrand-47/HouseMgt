import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'MagicianProgrammer474745845@#45')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
