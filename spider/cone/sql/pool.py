import pymysql
import sqlite3
from DBUtils.PooledDB import PooledDB


class Sql:
    def __init__(self, connection):
        self.conn = connection
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()


class MysqlPool():
    def __init__(self, host=None, db=None,user=None, pwd=None, port=None):
        self._pool = PooledDB(pymysql, maxconnections=0, host=host, user=user, passwd=pwd, db=db, port=port)

    def get_sql(self):
        return Sql(self._pool.connection())

    def close(self):
        self._pool.close()



class SqlitePool:
    def __init__(self, host=None, db=None,user=None,pwd=None):
        self._pool = PooledDB(sqlite3, 10, database=db, check_same_thread=False)

    def get_sql(self):
        return Sql(self._pool.connection())