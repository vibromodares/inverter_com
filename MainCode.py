import os
import sys
from datetime import datetime

from PyQt5.QtWidgets import QApplication

from app.logging.model.log_model import LoggingModel
from app.ResourcePath.app_provider.admin.main import resource_path as rp


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


path = resource_path("")
path = path.replace(path[2], "/")

# log_path_main = os.path.join(path, "files/logs/")
log_path_main = rp("files/logs/")

if __name__ == "__main__":
    from files.data.make_db import handle_db

    handle_db()

    app = QApplication(sys.argv)
    from core.app_provider.admin.main import Main

    main = Main()
    sys.exit(app.exec_())
else:
    log_name = datetime.now().strftime("%Y_%m_%d-%H_%M_%S")
    log_path = log_path_main + log_name + "/"
    os.makedirs(resource_path(log_path), exist_ok=True)
    logging_system = LoggingModel(str(log_path))
    logging_system.start_thread()
