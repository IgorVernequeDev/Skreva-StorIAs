import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    OPENROUTER_API_KEY = os.getenv('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')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///stories.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
