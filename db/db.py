import sqlite3
from flask import current_app
from sqlite3 import Error


class DB:
    # ref: https://www.sqlitetutorial.net/sqlite-python/create-tables/
    _curapp = None
    _dbpath = None
    _conn = None
    _maxid = 0

    def __init__(self) -> None:
        self._curapp = current_app
        self._get_settings()
        self._conn = self._create_connection()
        self._create_systems_table()
        if self._systems_records() <= 0:
            self._create_empty_systems()
            self.insert_system(1, 'systemname', '1.2.3.4', 'http://systemname', 'misc', 'other')

    def _commit(self):
        if self._conn is not None:
            self._conn.commit()
        return

    def _get_settings(self):
        self._dbpath = self._curapp.config['DATABASE_PATH']

    def dbpath(self) -> str:
        return self._dbpath

    def _create_connection(self):
        """ create a database connection to the SQLite database
            specified by db_file
        :param db_file: database file
        :return: Connection object or None
        """
        conn = None
        try:
            conn = sqlite3.connect(self._dbpath)
            return conn
        except Error as e:
            print(e)

        return conn

    def _create_systems_table(self):
        try:
            c = self._conn.cursor()
            cmd = """ CREATE TABLE IF NOT EXISTS systems (
                        id integer PRIMARY KEY,
                        name text NOT NULL,
                        ip text,
                        url text,
                        systype text,
                        location text
                    ); """
            c.execute(cmd)
        except Error as e:
            print(e)
        return

    def _systems_records(self):
        # ref https://www.sqlitetutorial.net/sqlite-python/sqlite-python-select/
        num = 0
        try:
            c = self._conn.cursor()
            cmd = 'Select count(*) from systems;'
            c = c.execute(cmd)
            rows = c.fetchall()

            for row in rows:
                num = num + row[0]

        except Error as e:
            print(e)

        return num

    def _create_empty_systems(self):
        try:
            c1 = self._conn.cursor()
            c2 = self._conn.cursor()
            cmd1 = 'insert into systems (id, name) values (1, "test");'
            cmd2 = 'delete from systems where id = 1;'
            c1.execute(cmd1)
            c2.execute(cmd2)
            self._commit()

        except Error as e:
            print(e)
        return

    def insert_system(self, id, name, ip, url, systype, location):
        try:
            cmd = 'insert into systems (id, name, ip, url, systype, location) values ' \
                  '( ?, ?, ?, ?, ?, ?);'
            c = self._conn.cursor()
            c.execute(cmd, (id, name, ip, url, systype, location))
            self._commit()

        except Error as e:
            print(e)
        return

    def load_systems(self) -> []:
        systems = []
        try:
            cmd = 'select id, name, ip, url, systype, location from systems;'
            c = self._conn.cursor()
            c = c.execute(cmd)
            rows = c.fetchall()

            for row in rows:
                one = {
                    "id": row[0],
                    "name": row[1],
                    "ip": row[2],
                    "url": row[3],
                    "systype": row[4],
                    "location": row[5]
                }
                systems.append(one)

        except Error as e:
            print(e)
        return systems

    def load_one_system(self, sys_id) -> {}:
        system = {}
        try:
            cmd = 'select id, name, ip, url, systype, location from systems where id = ?;'
            c = self._conn.cursor()
            c = c.execute(cmd, sys_id)
            row = c.fetchone()

            system = {
                "id": row[0],
                "name": row[1],
                "ip": row[2],
                "url": row[3],
                "systype": row[4],
                "location": row[5]
            }

        except Error as e:
            print(e)

        return system

    def save_one_system(self, sys_id, sys_name, sys_ip, sys_url, sys_type, sys_location):
        try:
            cmd = 'update systems set id = ?, name = ?, ip = ?, url = ?, systype = ?, location = ? where id = ?;'
            c = self._conn.cursor()
            c.execute(cmd, (sys_id, sys_name, sys_ip, sys_url, sys_type, sys_location, sys_id))
            self._commit()

        except Error as e:
            print(e)

        return None

    def add_system(self) -> int:
        try:
            cmd = 'select max(id) as num from systems;'
            c = self._conn.cursor()
            c = c.execute(cmd)
            row = c.fetchone()
            max_id = row[0]
            new_id = 0

            # now insert new record.
            new_id = max_id + 1
            cmd = 'insert into systems (id, name) values (?, ?);'
            c.execute(cmd, (new_id, ''))
            self._commit()

        except Error as e:
            print(e)

        return new_id

