import os
import json
import uuid
from abc import ABC
import sqlite3

from Shared.Infrastructure_Abstractions.ContextRepository import ContextRepository


class SqliteContextRepository(ContextRepository, ABC):
    def __init__(self):
        self.config = {}
        current_directory = os.getcwd()
        abspath = os.path.abspath(__file__)
        dname = os.path.dirname(abspath)
        os.chdir(dname)
        with open('../../../ReservationApi/config.json', 'r') as f:
            self.config = json.load(f)

        os.chdir(current_directory)

    @staticmethod
    def _table_exists(table_name, conn):
        cur = conn.cursor()
        sql_stmt = "SELECT name from sqlite_master WHERE type ='table' AND name = '" + table_name + "'"
        cur.execute(sql_stmt)
        rows = cur.fetchall()
        if len(rows) == 0:
            return False

        return True

    def _build_update_statement(self, read_model, key_name):
        table_name = type(read_model).__name__
        update_script = 'update ' + table_name + ' set '
        for key in read_model.__dict__.keys():
            update_script = update_script + key + "='" + str(read_model.__dict__[key]) + "', "
        update_script = update_script[0:-2]
        update_script = update_script + f" where {key_name} = '{read_model.__dict__[key_name]}'"
        return update_script

    def _build_insert_statement(self, read_model, key_name):
        table_name = type(read_model).__name__
        insert_script = 'insert into ' + table_name + ' ('
        values_clause = ' VALUES ('
        for key in read_model.__dict__.keys():
            insert_script = insert_script + key + ', '
            values_clause += f"'{str(read_model.__dict__[key])}', "

        insert_script = insert_script[0:-2] + ')' + values_clause[0:-2] + ')'
        return insert_script

    def _create_table(self, read_model, conn, key_name):
        table_name = type(read_model).__name__
        table_creation_script = 'create  table ' + table_name + '('
        for key in read_model.__dict__.keys():
            table_creation_script = table_creation_script + key + ' text '
            if key == key_name:
                table_creation_script += ' PRIMARY KEY'
            table_creation_script += ', '
        table_creation_script = table_creation_script[0:-2] + ')'
        conn.execute(table_creation_script)

    def _upsert_row(self, read_model, conn, key_name='Id'):
        update_script = self._build_update_statement(read_model, key_name)
        insert_script = self._build_insert_statement(read_model, key_name)
        cursor = conn.cursor()

        cursor.execute(update_script)
        if cursor.rowcount == 0:
            cursor.execute(insert_script)
        conn.commit()

    def _build_query_statement(self, read_model, query_model):
        select_stmt = "select * from " + type(
            read_model).__name__ + " where "
        for key in read_model.__dict__.keys():
            if key in query_model.__dict__.keys():
                select_stmt += f"{key} = '{query_model.__dict__[key]}' AND "

        return select_stmt[0:-4]

    def Save(self, read_model, key_name='Id'):
        database_name = self.config['reservationdb']
        conn = sqlite3.connect(database_name)
        if not self._table_exists(type(read_model).__name__, conn):
            self._create_table(read_model, conn, key_name)
        self._upsert_row(read_model, conn, key_name)

    def Read(self, read_model, query_model, primary_key_name="Id"):
        database_name = self.config['reservationdb']
        conn = sqlite3.connect(database_name)
        if not self._table_exists(type(read_model).__name__, conn):
            self._create_table(read_model, conn, primary_key_name)
        select_stmt = self._build_query_statement(read_model, query_model)
        cursor = conn.cursor()
        cursor.execute(select_stmt)
        r = [dict((cursor.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cursor.fetchall()]
        cursor.connection.close()
        if len(r) > 0:
            json_text = json.dumps(r[0])
            read_model.__dict__ = json.loads(json_text)

        return read_model

    def ReadQuery(self, read_model, query, key_name='Id'):
        database_name = self.config['reservationdb']
        conn = sqlite3.connect(database_name)
        if not self._table_exists(type(read_model).__name__, conn):
            self._create_table(read_model, conn, key_name)
        cursor = conn.cursor()
        cursor.execute(query)
        r = [dict((cursor.description[i][0], value) \
                  for i, value in enumerate(row)) for row in cursor.fetchall()]
        cursor.connection.close()
        if len(r) > 0:
            return r

        return None


if __name__ == '__main__':
    from Reservations.Domain.ReadModels.Reservation.ReservationReadModel import ReservationReadModel
    from Reservations.Domain.Models.Queries import FindReservationQuery

    reservation_id = str(uuid.uuid4())
    hotel_id = str(uuid.uuid4())
    room_type = 'Presidential'
    read_model_dictionary = {'Id': reservation_id, 'HotelId': str(uuid.uuid4()), 'RoomType': 'Presidential',
                             'IsActive': True}
    t_read_model = ReservationReadModel(read_model_dictionary)
    repo = SqliteContextRepository()
    repo.Save(t_read_model)
    sql_stmt = "select count(*) from " + type(t_read_model).__name__ + " where RoomType='" + t_read_model.RoomType + "'"
    data = repo.ReadQuery(t_read_model, sql_stmt)
    print(data)
    t_query = FindReservationQuery({"HotelId": hotel_id, 'Id': reservation_id})
    data = repo.Read(t_read_model, t_query)
    print(data)
    print(json.dumps(data.__dict__))
