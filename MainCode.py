import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


path = resource_path("")
path = path.replace(path[2], "/")

database_db_path = './files/logs/'
log_name = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
log_path = database_db_path + log_name + "/"

if __name__ == "__main__":

    app = QApplication(sys.argv)
    from core.app_provider.admin.main import Main

    main = Main()

    sys.exit(app.exec_())
else:
    from app.logging.model.log_model import LoggingModel

    logging_system = LoggingModel(str(log_path))
    logging_system.start_thread()
