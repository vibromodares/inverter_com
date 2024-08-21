from app.logging.model.data_log_model import DataLoggingModel


def plot_figure():
    import os
    log_path = './files/logs/2024_08_21-09_52_23/'
    files = os.listdir(log_path)
    files.remove('log.json')
    for file in files:
        if file.endswith('.json'):
            name = file.replace('.json', '')
            db = DataLoggingModel(name, log_path)
            db.plot_figure()
