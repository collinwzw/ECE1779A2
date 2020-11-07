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
    def delete_all_data(table,returnHTML):
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
            return render_template(returnHTML, message="database error: " + str(e))
        dbManager.teardown_db()
