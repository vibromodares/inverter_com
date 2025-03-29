from MainCode import path
from core.theme.color.color import pb_text_color_active, line_edit_bg, line_edit_text_color, label_text_color, \
    pb_bg_color_active, label_text_bg, login_text_color, login_bg_color, login_border_color, trade_on_bg_color, \
    trade_on_text_color, trade_off_text_color, trade_off_bg_color, trade_none_bg_color, trade_none_text_color, \
    login_forget_pb_bg, login_forget_pb_text, stop_trading_pb_bg_color, login_enter_pb_text, balance_label_text_color, \
    start_trading_pb_bg_color, login_enter_pb_bg, activate_account_pb_bg_color, hover_start_trading_pb_bg_color, \
    hover_stop_trading_pb_bg_color, make_db_bg, make_db_text_color

line_edit_style = "background-color: " + line_edit_bg + ";color: " + line_edit_text_color + ";border-radius: 7;"
line_edit_prop_style = "background-color: " + line_edit_bg + ";color: rgba(70, 240, 60, 255);"
label_style = "background-color: " + label_text_bg + ";color: " + label_text_color + ";border-radius: 7;"

balance_label_style = "background-color: " + label_text_bg + ";color: " + balance_label_text_color + \
                      ";border-radius: 7;"

active_pb_style = "QPushButton {background-color: " + pb_bg_color_active + ";" + "color: " + \
                  pb_text_color_active + ";border-radius: 7;} QPushButton:hover {background-color: #4C5569;}"

start_service_pb_style = "QPushButton {background-color: " + start_trading_pb_bg_color + ";" + "color: " + \
                         pb_text_color_active + ";border-radius: 7;} QPushButton:hover {background-color: " + \
                         hover_start_trading_pb_bg_color + ";}"

stop_service_pb_style = "QPushButton {background-color: " + stop_trading_pb_bg_color + ";" + "color: " + \
                        pb_text_color_active + ";border-radius: 7;} QPushButton:hover {background-color: " + \
                        hover_stop_trading_pb_bg_color + ";}"

close_pb_style = "QPushButton {border-image: url(" + path + \
                 "core/theme/pic/pic/close.png);} QPushButton:hover {background-color: #ea8e1e;}"

activate_account_pb_style = "QPushButton {background-color: " + activate_account_pb_bg_color + ";" + "color: " + \
                            pb_text_color_active + ";border-radius: 7;} QPushButton:hover {background-color: #4F8B63;}"

activate_label_main_style = "background-color: " + line_edit_bg + ";color: " + label_text_color + ";border-radius: 7;"

optimal_strategy_rb_style = "QRadioButton {background-color: " + line_edit_bg + ";color: " + label_text_color + ";border-radius: 7;} QRadioButton::indicator:checked{border-image: url(" + path + "core/theme/pic/pic/radio-button-green.png);width : 24px;height : 24px;}QRadioButton::indicator{width : 24px;height : 24px;}"
optimal_strategy_label_style = "background-color: " + line_edit_bg + ";color: " + line_edit_text_color + \
                               ";border-radius: 7;"
login_page_style = "background-color: " + login_bg_color + ";color: " + login_text_color + ";" + \
                   "border-radius : 7;border : 1px solid " + login_border_color + ";"
trade_none_style = "background-color:" + trade_none_bg_color + ";color: " + trade_none_text_color + ";"
trade_on_style = "background-color:" + trade_on_bg_color + ";color: " + trade_on_text_color + ";"
trade_off_style = "background-color: " + trade_off_bg_color + ";color: " + trade_off_text_color + ";"
login_forget_style = "background-color: " + login_forget_pb_bg + ";" + "color: " + login_forget_pb_text + ";"
login_enter_pb_style = "background-color: " + login_enter_pb_bg + ";" + "color: " + login_enter_pb_text + \
                       ";border-radius : 5;padding-bottom: 1px;"

inverter_unknown_stylesheet = "background-color: rgb(255, 85, 0);"
inverter_disconnect_stylesheet = "background-color: rgb(255, 0, 0);"
inverter_connect_stylesheet = "background-color: rgb(0, 255, 127);"
ui_line_style = "color: rgb(0, 255, 127);"
no_error_label = 'color: white;background-color: green;'
yes_error_label = 'color: white;background-color: red;'

start_inverter_pb_style = "QPushButton {background-color: " + start_trading_pb_bg_color + ";" + "color: " + \
                          pb_text_color_active + ";border-radius: 7;height : 30px;font: 9pt;} QPushButton:hover {background-color: " + \
                          hover_start_trading_pb_bg_color + ";}"
stop_inverter_pb_style = "QPushButton {background-color: " + stop_trading_pb_bg_color + ";" + "color: " + \
                         pb_text_color_active + ";border-radius: 7;height : 30px;font: 9pt;} QPushButton:hover {background-color: " + \
                         hover_stop_trading_pb_bg_color + ";}"

progress_bar_style = '''
#RedProgressBar {
    text-align: center;
    background-color: #E0E0E0;
}
#RedProgressBar::chunk {
    background-color: #F44336;
        width: 10px; 
    margin: 0.5px;
}
#GreenProgressBar {
    min-height: 12px;
    max-height: 12px;
    border-radius: 6px;
}
#GreenProgressBar::chunk {
    border-radius: 6px;
    background-color: #009688;
}
#BlueProgressBar {
    text-align: center;
    border: 2px solid #2196F3;
    border-radius: 5px;
}
#BlueProgressBar::chunk {
    background-color: #2196F3;
}
'''

progress_bar_format = "data insert  {percentage:.2f}% ({inserted} /{total})"
progress_bar_finished_format = "data insert finished"

make_db_stylesheet = "background-color: " + make_db_bg + ";color: " + make_db_text_color + ";MakeDBUIModel {background: #002025;border-radius: 20px;opacity: 100;border: 2px solid #ff2025;}"
