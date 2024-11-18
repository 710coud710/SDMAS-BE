
import os

class Config:

    DB_HOST = os.getenv('DB_HOST', 'serverless-europe-west2.sysp0000.db2.skysql.com')
    DB_PORT = os.getenv('DB_PORT', 4007)
    DB_USER = os.getenv('DB_USER', 'dbpgf16628416')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'Z)Gdq8uU0J9gzFUPQXlhwfglV')
    DB_NAME = os.getenv('DB_NAME', 'sdmas_db')
    DB_SSL_VERIFY = True
    
    SECRET_KEY = 'xincahfokey' 