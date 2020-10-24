import os


class Config:
    ENV = 'production'
    SECRET_KEY = os.urandom(32)
    HTTP_CLIENT_BASE_URL = 'http://0.0.0.0:3000'
    SERVER_BASE_URL = 'http://localhost:5000'
    MYSQL_HOST = 'bedkvxy0zoae2fzezgrj-mysql.services.clever-cloud.com'
    MYSQL_PORT = 3306
    MYSQL_USER = 'uijuxgeikmglyawn'
    MYSQL_PASSWORD = 'HNmjIdEckvUcIQFK9wk3'
    MYSQL_DB = 'bedkvxy0zoae2fzezgrj'




config = {
    'local': Config
}
