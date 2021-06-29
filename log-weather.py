#!/usr/bin/env python3

import bme280.i2c
import psycopg2
import contextlib

DB_PARAMS=''
DB_SEARCH_PATH='bme280'

@contextlib.contextmanager
def connect(dbParams=DB_PARAMS, dbSearchPath=DB_SEARCH_PATH):

    class Connection:
        def __init__(self, connection):
            self._connection = connection
        @contextlib.contextmanager
        def cursor(self):
            with self._connection.cursor() as cur:
                cur.execute(f'set search_path = {dbSearchPath}')
                yield cur

    with psycopg2.connect(dbParams) as con:
        yield Connection(con)

def insert(database, i2c):
    with database.cursor() as cur:
        cur.execute('''
            insert into t_bme280
                ( temperature
                , humidity
                , pressure
                )
            values
                ( %s
                , %s
                , %s
                )
        ''',
            ( i2c.temperature
            , i2c.humidity
            , i2c.pressure
            ))
            
def main():

    # get sensor data
    i2c = bme280.i2c.i2c()
    assert i2c.open()
    assert i2c.runForcedMode()

    # only connect to database if we actually have data
    with connect() as con:
        insert(con, i2c)

if __name__ == '__main__':
    main()
