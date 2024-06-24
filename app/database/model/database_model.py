from tinydb import TinyDB, table, Query
from tinydb.table import Table

database_db_path = './files/database/'  # TODO:poshe ro bayad aval besaze
database_file_name = 'database.json'  # TODO:poshe ro bayad aval besaze
database_table_name = 'database'


class DataBaseModel:
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
