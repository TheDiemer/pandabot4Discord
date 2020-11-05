#!/usr/bin/python3
import MySQLdb

class karma_api:
    # Init to handle the ip, user, password, and database
    def __init__(self, ip='localhost', username=None, password=None, db=None):
        if username is None or password is None:
            raise Exception("Username or Password were not supplied.")

        self.ip = ip
        self.username = username
        self.password = password
        self.db = db


    # Connect to the database, and setup a cursor if applicable
    def __connect(self, cursorOpen=False):
        conn = MySQLdb.connect(self.ip, self.username, self.password, self.db)
        if cursorOpen:
            cursor = conn.cursor()
        else:
            cursor = None
        return (conn, cursor)


    # Close the connection to the database as well as save and close any cursor if applicable
    def __close(self, conn=None, cursor=None):
        if cursor:
            conn.commit()
            cursor.close()
        conn.close()


    # get some data (ask) from the db
    def query(self, ask=None):
        if ask is None:
            return (False, None)
        else:
            conn, cursor = self.__connect(cursorOpen=False)
        conn.query(ask)
        result = conn.store_result()
        data = result.fetch_row(maxrows=0, how=1)
        self.__close(conn=conn)
        return data


    # make some modification on the db
    def modify(self, modification=None):
        if modification is None:
            return False
        conn, cursor = self.__connect(cursorOpen=True)
        cursor.execute(modification)
        self.__close(conn=conn, cursor=cursor)
        return True


    def checkAlias(self, person=None):
        if person is not None:
            conn, cursor = self.__connect(cursorOpen=False)
            data = self.query(ask="select * from alias where alias = '{0}'".format(person))
            self.__close(conn=conn)
            if data == ():
                return (False, None)
            for options in data:
                if person == options.get('alias'):
                    return (True, options.get('person'))
            return (False, None)
        else:
            return (False, None)


    def getRank(self, value=None, person=None):
        if value is None:
            return (False, None)
        else:
            conn, cursor = self.__connect(cursorOpen=False)
            if person is None:
                ask = "with order_val as (select person,{0},RANK() OVER(ORDER BY {0} desc) rank from karma) select * from order_val where rank = (select MIN(rank) from order_val);".format(value)
            else:
                ask = "with order_val as (select person,{0},RANK() OVER (Order By {0} desc) rank from karma) select * from order_val where person = '{1}';".format(value, person)
            data = self.query(ask=ask)
            self.__close(conn=conn)
            return data
