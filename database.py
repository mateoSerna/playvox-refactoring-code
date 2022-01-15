import logging

import mysql.connector
from mysql.connector import errorcode

import ssm

# I'd separate the database layer.
try:
    # I'd use some service such as SSM or KMS from Amazon to store this kind of sensitive data.
    # Never to expose this information.
    mysql_user = ssm.get("/mysql/username")
    mysql_password = ssm.get("/mysql/password")
    mysql_host = ssm.get("/mysql/host")
    mysql_port = ssm.get("/mysql/port")
    mysql_database = ssm.get("/mysql/database")
    
    connection = mysql.connector.connect(
        user=mysql_user,
        password=mysql_password,
        host=mysql_host,
        port=mysql_port,
        database=mysql_database,
    )
except mysql.connector.Error as err:
    # I'd use more specific exceptions.
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        logging.error("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        logging.error("Database does not exist")
    else:
        logging.error(err)
