import os

class BaseConfig:
    """Base configuration"""
    TESTING = False
    # Disable signals to applications every time a change is about to be made to the database.
    SQLALCHEMY_TRACK_MODIFICATIONS = False 


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


# class TestingConfig(BaseConfig):
#     """Testing configuration"""
#     TESTING = True
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_TEST_URL')


# class ProductionConfig(BaseConfig):
#     """Production configuration"""
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')