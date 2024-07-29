from typing import Union

from app.database.model.database_model import DataBaseModel, DataModel
from app.database.model.inverter_model import InverterModel

device_models_db = DataBaseModel(file_name='device_models.json')
device_list_db = DataBaseModel(file_name='device_list.json')


def get_all_module() -> list[str]:
    return device_list_db.get_all_data()


def get_all_module_model() -> list[InverterModel]:
    modules_config = device_models_db.get_all_data()
    modules = []
    for module_config in modules_config:
        modules.append(InverterModel(module_config['model_id'], module_config['name'], module_config['com_disc']))
    return modules


def get_module_by_id(model_id: int) -> InverterModel:
    module_config = device_models_db.DB.get(device_models_db.query.model_id == model_id)
    return InverterModel(module_config['model_id'], module_config['name'], module_config['com_disc'])


def get_device_by_id(inverter_id: int):
    module_config = device_list_db.DB.get(device_list_db.query.inverter_id == inverter_id)
    device = get_module_model(module_config['model_id'])

    return device(module_config)


def get_module_model(model_id: int):
    from app.inverter.iG5A.iG5AModel_new import iG5AModel
    module = get_module_by_id(model_id)
    name = module.name
    if name == 'iG5A':
        return iG5AModel

    return None


def get_db_by_model_id(model_id) -> DataModel:
    database_table_name = get_module_by_id(model_id).name
    return DataModel(database_table_name)
