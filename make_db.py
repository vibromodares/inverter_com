import pandas as pd
from app.database.model.database_model import DataBaseModel

def make_tinydb_from_excel():
    df = pd.read_excel('files/data/first_data.xlsx')

    database_db_path = './files/data/database.json'
    database_table_name = 'database'
    print(df)
    db = DataBaseModel(database_db_path,database_table_name)
    # db.insert_data({
    #     'parameter_name': 'Inverter Model',
    #     'address': '0x0300',
    #     'byte': '0x000A',
    #     'discreption': 'iG5A',
    # })


make_tinydb_from_excel()
