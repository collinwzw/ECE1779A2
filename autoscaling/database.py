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
    def get_db():
        # access to database
        if 'db' not in g:
            g.db = database.connect_to_database()

        return g.db


    @staticmethod
    def delete_all_data(table):
        '''method delete all data in one table'''
        db = database.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("truncate table " + table)
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            return render_template("error.html", message="database error: " + str(e))

    @staticmethod
    def fetch_autoscaling_parameter():
        db = database.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM autoscaling "
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except:
            e = sys.exc_info()
            db.rollback()
            return render_template("error.html", message="database error: " + str(e))
