# -*- coding: UTF-8 -*-

from __future__ import absolute_import, division, print_function

import datetime
import MySQLdb as my
import logging
import re
import time
import sys
import json

logging.basicConfig(format="%(asctime)-15s %(name)s: %(levelname)s: %(message)s")
logger = logging.getLogger("DB")
logger.setLevel(logging.DEBUG)


class DB(object):
    re_display = re.compile("[ \n]+", re.IGNORECASE)

    def __init__(self, host="localhost", user="", passwd="", db="test", use_result=False, connect_timeout=10, use_unicode=True, dict_result=False):

        self.ci = {
            "host": host,
            "user": user,
            "passwd": passwd,
            "db": db,
            "charset": "utf8",
            "use_unicode": use_unicode,
            "connect_timeout": connect_timeout
        }
        self.conn = my.connect(**self.ci)
        if dict_result:
            self.curs = self.conn.cursor(cursorclass=my.cursors.SSDictCursor)
        else:
            self.curs = self.conn.cursor(cursorclass=my.cursors.SSCursor)
        logger.info("connected to %(user)s@%(host)s:%(db)s" % self.ci)

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return "%(user)s@%(host)s/%(db)s" % self.ci

    def __str__(self):
        return self.__unicode__()

    def close(self):
        self.conn.close()
        logger.info("Closed connection to %s" % self)

    def showWarnings(self):
        return self.conn.show_warnings()

    def getHeaders(self):
        if self.curs.description:
            return [i[0] for i in self.curs.description]
        return None

    def query(self, qry):
        start = time.time()
        try:
            self.curs.execute(qry)
            ret = self.curs.fetchall()
            logger.debug("[%.4fs] %s, %s" % ((time.time() - start), self, self.re_display.sub(" ", qry)[0:1000]))
            self.conn.commit()
            return ret
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            logger.error("line %s, %s" % (exc_traceback.tb_lineno, str(e)))
            raise e

    def hquery(self, qry):
        return self.query(qry), self.getHeaders()

    def rows_affected(self):
        return self.curs.rowcount

    def getRowsAffected(self):
        return self.curs.rowcount

    def getLastRowId(self):
        return self.curs.lastrowid

    @staticmethod
    def sqlwrap(text):
        return "NULL" if text is None else json.dumps(text)

    @staticmethod
    def sqlize(x):
        if x is None:
            return "NULL"
        elif isinstance(x, (int, long, float)):
            return str(x)
        elif isinstance(x, datetime.datetime):
            return x.strftime("'%Y-%m-%d %H:%M:%S'")
        elif isinstance(x, datetime.date):
            return x.strftime("'%Y-%m-%d'")
        else:
            return DB.sqlwrap("%s" % x.encode("utf8"))
