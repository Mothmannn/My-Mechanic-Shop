class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:536665@localhost/mechanic_db'
    DEVUG = True

class TestingConfig:
    pass

class ProductionConfig:
    pass