import os
import sys
from PyQt5.QtWidgets import QApplication

from app.inverter.iG5A.iG5A_model import iG5AModel

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


path = resource_path("")
path = path.replace(path[2], "/")

if __name__ == "__main__":
    # iG5A = iG5AModel()

    app = QApplication(sys.argv)
    from core.app_provider.admin.main import Main

    main = Main()
    sys.exit(app.exec_())

    # start_time = time()
    # print(serial.readSerial('01R00001A4'))
    # print(time() - start_time)
    # start_time = time()
    # print(serial.readSerial('01R03001A7'))
    # print(time() - start_time)
    # print(serial.readSerial('01R03011A8'))
    # print(serial.readSerial('01W0380101F48F'))
    # print(serial.readSerial('01W03821000177'))
    #
    # sleep(2)
    # print(serial.readSerial('01R030D1A8'))
    # sleep(2)
    # print(serial.readSerial('01W03821000076'))
