from app.database.model.database_model import DataBaseModel


def get_all_module() -> list[str]:
    db = DataBaseModel(file_name='inverter_list.json')
    return db.get_all_data()

def get_all_module_model() -> list[str]:
    db = DataBaseModel(file_name='inverter_models.json')
    return db.get_all_data()
