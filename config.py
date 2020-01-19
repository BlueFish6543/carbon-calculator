import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret'
    UPLOAD_FOLDER = os.path.join('static', 'tmp')