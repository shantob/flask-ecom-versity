import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-unique-secret-key-2024'
    SESSION_PERMANENT = True
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

class DevelopmentConfig(Config):
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}