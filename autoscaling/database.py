import mysql.connector
from flask import render_template, g
import sys


db_config = {'user': 'admin',
             'password': 'ece1779pass',
             'host': 'data.cbimjtv4anpd.us-east-1.rds.amazonaws.com',
             'database': 'user'}

class database:
    @staticmethod
    def connect_to_database():
        # Connect database
        return mysql.connector.connect(user=db_config['user'],
                                       password=db_config['password'],
                                       host=db_config['host'],
                                       database=db_config['database'])

    @staticmethod
    def fetch_autoscaling_parameter():
        """get the parameter from database"""
        db = database.connect_to_database()
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM autoscaling "
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result