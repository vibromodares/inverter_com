from app.ResourcePath.app_provider.admin.main import resource_path
import os
from tinydb import TinyDB
import hashlib

config_path = "files/config/"
config_db_name = 'config.json'
config_table_name = 'config'

developer = 1

os.makedirs(resource_path(config_path), exist_ok=True)

config_db_path = resource_path(config_path + config_db_name)
config_db = TinyDB(config_db_path)
config_db.drop_tables()
config_db = TinyDB(config_db_path).table(config_table_name)


# start  format Config
time_format = '%Y-%m-%d %H:%M:%S'
config_db.insert({"time_format": str(time_format)})

# Start  Developer Config
if developer:
    developer_config = hashlib.md5(b'VamPire1468').digest()
else:
    developer_config = ""

config_db.update({"developer_config": str(developer_config)})
# end  Developer Config

print("config Create Successfully")
