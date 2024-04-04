class Config(object):
    DEBUG = False
    FIREWORKS_API_KEY = "SqBWv34DVdUJFGpIWO6IXvgDzCpeHvjMXcsRm6IIJScUGOHx"
    DB_PATH = "app/data/outlets.db"


class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
