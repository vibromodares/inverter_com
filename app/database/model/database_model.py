from tinydb import TinyDB, table, Query
from tinydb.table import Table

database_db_path = './files/database/'  # TODO:poshe ro bayad aval besaze
database_file_name = 'database.json'  # TODO:poshe ro bayad aval besaze
database_table_name = 'database'


class DataBaseModel:
    DB: Table

    def __init__(self, db_path: str = None, file_name: str = None, table_name: str = None):
        if db_path is None or table_name is None:
            self.db_path = database_db_path
            self.table_name = database_table_name
        else:
            self.db_path = db_path
            self.table_name = table_name

        if file_name is None:
            self.file_name = database_file_name
        else:
            self.file_name = file_name

        self.query = Query()
        self.DB = TinyDB(self.db_path + self.file_name).table(self.table_name)

    def get_response(self, model_id, address, byte):
        dataProp = Query()
        return self.DB.get((dataProp.address == address) & (dataProp.byte == byte))

    def insert_data(self, data):
        self.DB.insert(data)

    def get_all_data(self):
        return self.DB.all()

    def drop_all_data(self):
        TinyDB(self.db_path + self.file_name).drop_table(self.table_name)

    def __repr__(self):
        return self.DB.__repr__()


class DataModel:
    DB: Table

    def __init__(self, table_name: str):
        database_db_path_data = './files/data/'
        database_file_name_data = 'database.json'

        self.table_name = table_name
        self.db_path = database_db_path_data
        self.file_name = database_file_name_data

        self.query = Query()
        self.DB = TinyDB(self.db_path + self.file_name).table(self.table_name)

    def get_responses(self, address: str, byte: str = None, range_in: str = None):
        dataProp = Query()

        if byte is None:
            if range_in is None:
                return self.DB.search((dataProp.address == address))
            else:
                return self.DB.search((dataProp.address == address) & (dataProp.range == range_in))
        else:
            if range_in is None:
                return self.DB.search(
                    (dataProp.address == address) & (dataProp.allotment_for_bits == byte))
            else:
                return self.DB.search(
                    (dataProp.address == address) &
                    (dataProp.range == range_in) &
                    (dataProp.allotment_for_bits == byte))

    def get_all_data(self):
        return self.DB.all()

    def drop_all_data(self):
        TinyDB(self.db_path + self.file_name).drop_table(self.table_name)

    def __repr__(self):
        return self.DB.__repr__()
