#!/usr/bin/env python3

import am2302
import psycopg2
import contextlib

DB_PARAMS=''
DB_SEARCH_PATH='am2302'

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

def insert(database, am2302_data):
    with database.cursor() as cur:
        cur.execute('''
            insert into t_am2302
                ( temperature
                , humidity
                )
            values
                ( %s
                , %s
                )
        ''',
            ( am2302_data.temperature
            , am2302_data.humidity
            ))
            
def main():

    # get sensor data
    d = am2302.read(pin=7, retries=20)

    # only connect to database if we actually have data
    if d is not None:
        print(f'Temperature: {d.temperature}°C, humidity: {d.humidity}%')
        with connect() as con:
            insert(con, d)

if __name__ == '__main__':
    main()
