import logging

import pymysql
from pymysql.cursors import DictCursor

from apiException.diy_exception import *
from config.config import *


class Database:         #在外部进行实例化Database()时，会自动将__init__中定义的函数参数传进（），以便后续调用

    def __init__(self):
        #对于在外部不会被调用，只在类内部被调用的属性/方法，可以__进行私有化
        self.__db = self.__get_connect()

    @staticmethod
    def __get_connect():
        try:
            conn = pymysql.Connect(
                host=DB_HOST,
                port=DB_PORT,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD,
                charset="utf8",
                autocommit=True
            )
            return conn
        except Exception as e:
            logging.error(f"数据库连接失败，错误异常是{e}")
            raise DatabaseException()

    def get_one(self, sql):
        try:
            if self.__db:
                with self.__db.cursor(DictCursor) as cur:
                    cur.execute(sql)
                    return cur.fetchone()
        except Exception as e:
            logging.error(f"数据库查询失败，错误异常是{e}")
            raise GetDataException()

    def execute_sqls(self, *sqls):
        try:
            if self.__db:
                with self.__db.cursor(DictCursor) as cur:
                    for sql in sqls:
                        cur.execute(sql)
        except Exception as e:
            logging.error(f"数据库修改/删除失败，错误异常是{e}")
            raise ExecuteSqlException()

