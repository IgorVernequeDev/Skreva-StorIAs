import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    OPENROUTER_API_KEY = os.getenv('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')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///stories.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
