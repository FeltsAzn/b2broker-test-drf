import os
import time

import MySQLdb

# MySQL credentials
USER = os.getenv("MYSQL_USER")
PASSWORD = os.getenv("MYSQL_PASSWORD")
HOST = os.getenv("MYSQL_HOST")
DB = os.getenv("MYSQL_DATABASE")
TRY_AMOUNT = int(os.getenv("CONNECTION_TRYING_AMOUNT", 5))


def check_mysql_connection(tries: int = TRY_AMOUNT) -> None:
    print("Checking MySQL Connection...")
    while tries:
        try:
            db = MySQLdb.connect(user=USER, passwd=PASSWORD, host=HOST, db=DB)
            print("MySQL is up.")
            db.close()
            break
        except MySQLdb.OperationalError:
            print("Failed to connect to MySQL, retrying in 2 seconds...")
            time.sleep(2)
            tries -= 1


check_mysql_connection()
