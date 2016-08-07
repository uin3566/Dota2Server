# -*- coding:utf-8 -*-

__author__ = 'Fang.Xu'

from MySQLdb import OperationalError

global sql_operator


def sqlFunc(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as e:
            if 'MySQL server has gone away' in str(e):
                sql_operator.connect()
                return func(*args, **kwargs)
            print e
    return wrapper
