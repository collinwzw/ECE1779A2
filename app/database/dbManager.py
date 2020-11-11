import mysql.connector
from flask import render_template,g
import sys
from app.database.db_config import db_config


class dbManager:

    @staticmethod
    def get_db():
        #access to database
        db = getattr(g, '_database', None)
        if db is None:
            db = g._database = dbManager.connect_to_database()
        return db

    @staticmethod
    def teardown_db(exception):
        #close the database
        db = getattr(g, '_database', None)
        if db is not None:
            db.close()

    @staticmethod
    def connect_to_database():
        #Connect database
        return mysql.connector.connect(user=db_config['user'],
                                       password=db_config['password'],
                                       host=db_config['host'],
                                       database=db_config['database'])

    @staticmethod
    def delete_all_data(table):
        '''method delete all data in one table'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("truncate table "+table)
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))



    @staticmethod
    def updata_autoscaling_parameter(key, value):
        '''update autocaling table date'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "update autoscaling set parameter = %s WHERE item = %s"
            cursor.execute(query, (value, key))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))

    @staticmethod
    def updata_autoscaling_parameter(key, value):
        '''update autocaling table date'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "update autoscaling set parameter = %s WHERE item = %s"
            cursor.execute(query, (value, key))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))

    @staticmethod
    def fetch_autoscaling_parameter(name):
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM autoscaling WHERE name = %s "
            cursor.execute(query, (name,))
            result = cursor.fetchone()
            return result
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))

    @staticmethod
    def checkuser(username):
        '''method search data in SQL with target condition'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM accounts WHERE username = %s"
            cursor.execute(query, (username,))
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))