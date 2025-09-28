import os

MYSQL_URL = os.getenv("MYSQL_URL", "jdbc:mysql://172.22.1.2:3306/elysium")
MYSQL_USER = os.getenv("MYSQL_USER", "root")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "123456")
MYSQL_DRIVER = "com.mysql.cj.jdbc.Driver"   

MONGO_URI = os.getenv("MONGO_URI", "mongodb://172.15.0.3:27017/elysium_db")

LOCALSTACK_ENDPOINT = os.getenv("LOCALSTACK_ENDPOINT", "http://localhost:4566")
S3_BUCKET = os.getenv("S3_BUCKET", "motivo-de-decisao")
S3_PREFIX = os.getenv("S3_PREFIX", "analises/")

MAX_FILE_SIZE_BYTES = int(os.getenv("MAX_FILE_SIZE_BYTES", 1 * 1024 * 1024))