import os
from time import sleep
from datetime import datetime
from threading import Thread
from typing import Callable

import singleton
from MainCode import path
# from core.config.Config import db_path, logout_time
from core.model.MainUI import MainUi
from core.model.SplashScreen import SplashScreen
from core.theme.color.color import  login_line_edit_bg, login_line_edit_text, \
    login_line_edit_border, start_splash_align, start_splash_color, close_splash_align, close_splash_color, \
    start_splash_font_size, end_splash_font_size
from core.theme.pic import Pics


class Main:
    def __init__(self):
        super().__init__()
        self.start_splash = SplashScreen(path + "core/theme/pic/pic/start_splash.png", 500)
        self.start_splash.alignment = start_splash_align
        self.start_splash.color = start_splash_color
        self.start_splash.save_text_show = False
        self.start_splash.set_font(start_splash_font_size)

        self.close_splash = SplashScreen(path + "core/theme/pic/pic/close_splash.jpg", 500)
        self.close_splash.alignment = close_splash_align
        self.close_splash.color = close_splash_color
        self.close_splash.set_font(end_splash_font_size)

        self.start_splash.show()
        self.State_Render = False
        self.State_PLC = False
        self.stopCheckThread = False

        self.stopCheckRender = False
        self.stopCheckSender = False
        self.stopCheckPLC = False
        self.loginFlag = 0
        self.stop_Thread = False

        self.Thread = Thread(target=self.main_thread, args=(lambda: self.stop_Thread,))

        self.create_db_path()

        self.me = singleton.SingleInstance()
        self.main_ui = MainUi()

        self.start_splash.show_message("\t\t initializing database connection")

        # self.start_splash.show_message("starting Bale system")
        #
        # self.start_splash.show_message("starting shift system")
        #
        # self.start_splash.show_message("creating backup system")
        #
        # self.start_splash.show_message("starting line monitoring system")
        #
        #
        # self.start_splash.show_message("starting electrical substation system")
        #
        # self.start_splash.show_message("initializing DA units system")


        self.run_thread()


        self.start_splash.finish(self.main_ui)
        self.main_ui.show()

    def main_thread(self, stop_thread: Callable[[], bool]) -> None:
        while True:
            sleep(5)
            try:
                self.check_threads()
            except Exception as e:
                pass

    def run_thread(self):
        self.Thread.start()

    def check_plc_status(self):
        pass

    def check_threads(self):
        pass

    def stop_all_threads(self):
        pass


    def close(self):
        r = ""
        if r == "Success":
            self.close_splash.show()
            self.close_splash.show_message("start closing")
            self.stop_all_threads()
            self.close_splash.finish(self.main_ui)
            self.main_ui.close()
            os._exit(0)

    @staticmethod
    def create_db_path():
        from app.ResourcePath.app_provider.admin.main import resource_path as get_path

        # os.makedirs(get_path(db_path), exist_ok=True)
