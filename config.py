class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:536665@localhost/mechanic_db'
    DEBUG = True

class TestingConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///testing.db'
    TESTING = True
    DEBUG = True
    CACHE_TYPE = 'SimpleCache'

class ProductionConfig:
    pass