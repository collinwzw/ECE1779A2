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
    def updata_autoscaling_parameter(max_worker, min_worker, cooling_time, cpu_up_threshold, cpu_down_threshold, extend_ratio, shrink_ratio):
        '''update autocaling table date'''
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "update autoscaling set max_worker= %s ,min_worker= %s,cooling_time= %s,cpu_up_threshold= %s,cpu_down_threshold= %s,extend_ratio= %s,shrink_ratio= %s where name = config"
            cursor.execute(query, (max_worker, min_worker,cooling_time,cpu_up_threshold, cpu_down_threshold, extend_ratio, shrink_ratio))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))


    @staticmethod
    def fetch_autoscaling_parameter():
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        try:
            query = "SELECT * FROM autoscaling "
            cursor.execute(query)
            result = cursor.fetchall()
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
            account = cursor.fetchone()
            return account
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))

    @staticmethod
    def write_admin():
        db = dbManager.get_db()
        cursor = db.cursor(dictionary=True)
        username = "admin"
        password_hash = "pbkdf2:sha256:150000$NEDS8BFQ$7d7730a1563942bb85897c5dc5997a6d539b8cb9cfeaa2260d06f43f5f7cd7bd"
        email = "ece1779group@gmail.com"
        admin_auth = 1
        try:
            cursor.execute("Insert into accounts (username, password_hash, email,admin_auth) "
                           "values (%s, %s, %s, %s)", (username, password_hash, email, admin_auth))
            cursor.execute("commit")
        except:
            e = sys.exc_info()
            db.rollback()
            dbManager.teardown_db(e)
            return render_template("error.html", message="database error: " + str(e))
