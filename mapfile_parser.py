from __future__ import print_function
# from desktopmagic.screengrab_win32 \
#     import(getDisplayRects, saveScreenToBmp, getScreenAsImage, getRectAsImage, getDisplaysAsImages)
import sys
import os
import os.path
import threading
import time
from typing import Text
import pickle
import webbrowser
# import schedule
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
# from PyQt5 import uic
from datetime import datetime

import gui_image, icon_T
import map_parser
import db_connect
from subwindow import SubWindow
from send_email import gmail_sender
# ---------------------
VERSION = '20220209'
# ---------------------

LOGIN_PAGE_NO = 0
PROGRESS_PAGE_NO = 1
REGISTER_PAGE_NO = 2
LOGIN_STATUS = 0
duplicated_btn_checked = False

global news_list_info
USER_EMAIL = ''
USE_PROFILE = 0
news_list_info = []


def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class MainWindow(QDialog):
    def __init__(self):
        global news_list_info
        global USE_PROFILE
        global USER_EMAIL
        global LOGIN_STATUS

        super(MainWindow, self).__init__()

        # loadUi("login.ui", self)
        LOGIN_STATUS = 0  # 초기화

        login_ui_file = resource_path("login.ui")
        loadUi(login_ui_file, self)
        logo_pixmap = QPixmap(":/newPrefix/parser_title.png")
        self.label_title.setPixmap(QPixmap(logo_pixmap))

        logo_pixmap = QPixmap(":/newPrefix/logo_lg.png")

        self.label_logo.setPixmap(QPixmap(logo_pixmap))
        self.loginBTN.clicked.connect(self.open_login)
        self.registerBTN.clicked.connect(self.open_register)
        self.profile_checkBox.clicked.connect(self.checked_load_profile)
        # self.lineEdit_4.clicked.connect(self.open_webbrowser)
        self.radioButton_1.setHidden(True)
        self.radioButton_2.setHidden(True)
        self.radioButton_3.setHidden(True)
        self.radioButton_4.setHidden(True)
        self.radioButton_5.setHidden(True)
        self.radioButton_6.setHidden(True)
        # self.setWindowTitle('MapParser v.' + VERSION)

        profile_file = open('profile.pkl', 'rb')
        profile = pickle.load(profile_file)
        user_id = profile['email']
        passwd = profile['pass']
        profile_file.close()
        # print(f'[12/30] profile : {profile}')

        use_profile_file = open('use_profile.pkl', 'rb')
        profile_status = pickle.load(use_profile_file)
        use_profile_file.close()
        # print(f'[12/30] profile_status : {profile_status}')
        # profile_status = 1 #profile['use_profile']

        if profile_status == 1:
            USE_PROFILE = 1

            self.profile_checkBox.toggle()
            self.user_edit.setText(user_id)
            self.passwd_edit.setText(passwd)
        else:
            USE_PROFILE = 0
            self.user_edit.setText('')
            self.passwd_edit.setText('')

        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        # print(f'[12/13] news_list : {news_list_info}')
        # print(f'[12/13] news_list_counter : {news_list_counter}')

        counter = 0
        if counter == 0 and counter < news_list_counter:
            self.radioButton_1.setHidden(False)
            self.radioButton_1.setText(news_list_info[counter][0].lstrip())
            self.radioButton_1.clicked.connect(self.open_webbrowser_0)
            counter += 1
        else:
            self.radioButton_1.setHidden(True)

        if counter == 1 and counter < news_list_counter:
            self.radioButton_2.setHidden(False)
            self.radioButton_2.setText(news_list_info[counter][0].lstrip())
            self.radioButton_2.clicked.connect(self.open_webbrowser_1)
            counter += 1
        else:
            self.radioButton_2.setHidden(True)

        if counter == 2 and counter < news_list_counter:
            self.radioButton_3.setHidden(False)
            self.radioButton_3.setText(news_list_info[counter][0].lstrip())
            self.radioButton_3.clicked.connect(self.open_webbrowser_2)
            counter += 1
        else:
            self.radioButton_3.setHidden(True)

        if counter == 3 and counter < news_list_counter:
            self.radioButton_4.setHidden(False)
            self.radioButton_4.setText(news_list_info[counter][0].lstrip())
            self.radioButton_4.clicked.connect(self.open_webbrowser_3)
            counter += 1
        else:
            self.radioButton_4.setHidden(True)

        if counter == 4 and counter < news_list_counter:
            self.radioButton_5.setHidden(False)
            self.radioButton_5.setText(news_list_info[counter][0].lstrip())
            self.radioButton_5.clicked.connect(self.open_webbrowser_4)
            counter += 1
        else:
            self.radioButton_5.setHidden(True)

        if counter == 5 and counter < news_list_counter:
            self.radioButton_6.setHidden(False)
            self.radioButton_6.setText(news_list_info[counter][0].lstrip())
            self.radioButton_6.clicked.connect(self.open_webbrowser_5)
            counter += 1
        else:
            self.radioButton_6.setHidden(True)

        r = 0

        if db_connect.version_check(VERSION) == True:
            win = SubWindow(100)
            r = win.showModal()
            # print(f'[12/25] r : {r}')

        if r == 0:
            map_parser.init_dir()
        else:
            download_status = db_connect.download()
            if download_status == True:
                win = SubWindow(101)
                r = win.showModal()
                time.sleep(10)
                sys.exit()

    def open_webbrowser_0(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        # print(f'[12/15] group box clicked')
        url = news_list_info[0][1]
        webbrowser.open(url)

    def open_webbrowser_1(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[1][1]
        webbrowser.open(url)

    def open_webbrowser_2(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[2][1]
        webbrowser.open(url)

    def open_webbrowser_3(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[3][1]
        webbrowser.open(url)

    def open_webbrowser_4(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[4][1]
        webbrowser.open(url)

    def open_webbrowser_5(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[5][1]
        webbrowser.open(url)

    def checked_load_profile(self):
        global USE_PROFILE

        if self.profile_checkBox.isChecked() == True:
            use_profile_file = open('use_profile.pkl', 'wb')
            pickle.dump(1, use_profile_file)
            use_profile_file.close()
            # print(f'[12/30] onClick -> profile_status : 1')
        else:
            use_profile_file = open('use_profile.pkl', 'wb')
            pickle.dump(0, use_profile_file)
            use_profile_file.close()
            # print(f'[12/30] onClick -> profile_status : 0')

    def open_login(self):
        global USER_EMAIL
        global LOGIN_STATUS

        # db_connect.update_demo_date_test("test")
        # print(f'open_login: update_demo_date_test called. issue_date is modified for test email')

        user_id = self.user_edit.text()
        passwd = self.passwd_edit.text()
        USER_EMAIL = self.user_edit.text()

        db_connect.check_activate(user_id)
        if user_id != '' and passwd != '':
            # db_connect.check_expired_date(user_id)

            if db_connect.check_account(user_id, passwd) == True:

                if db_connect.check_demo_status(user_id) == True:  # 가입후 한달 이내
                    win = SubWindow(11)
                    r = win.showModal()
                    if r == 1:
                        LOGIN_STATUS = 1  # 한달 이내 demo
                        profile = db_connect.get_user_info(user_id)
                        # print(f'[12/22] Saved sprofile : {profile}')
                        profile_file = open('profile.pkl', 'wb')
                        profile_user_name = profile["email"]
                        # print(f'[12/22] Saved profile_user_name : {profile_user_name}')
                        pickle.dump(profile, profile_file)
                        profile_file.close()

                        USER_EMAIL = user_id

                        lastest_login_date = datetime.today().strftime('%Y-%m-%d')
                        # print(f'lastest_login_date : {lastest_login_date}')
                        db_connect.update_latest_login_date(
                            user_id, lastest_login_date)
                        db_connect.insert_log_data(
                            user_id, lastest_login_date)
                        # win = SubWindow(3)
                        # r = win.showModal()
                        # print(
                        #     f'[12/13] [open_login] widget.currentIndex() : {widget.currentIndex()}')
                        widget.setCurrentIndex(PROGRESS_PAGE_NO)
                else:  # 가입후 한달 지남
                    # 활성, 유효기간 남음
                    if db_connect.check_activate(user_id) == 1 and db_connect.check_expired_date(user_id) == True:
                        LOGIN_STATUS = 2  # 한달 이후 유효기간 남음
                        profile = db_connect.get_user_info(user_id)
                        # print(f'[12/22] Saved sprofile : {profile}')
                        profile_file = open('profile.pkl', 'wb')
                        profile_user_name = profile["email"]
                        # print(f'[12/22] Saved profile_user_name : {profile_user_name}')
                        pickle.dump(profile, profile_file)
                        profile_file.close()

                        USER_EMAIL = user_id

                        lastest_login_date = datetime.today().strftime('%Y-%m-%d')
                        # print(f'lastest_login_date : {lastest_login_date}')
                        db_connect.update_latest_login_date(
                            user_id, lastest_login_date)
                        db_connect.insert_log_data(
                            user_id, lastest_login_date)
                        # win = SubWindow(3)
                        # r = win.showModal()
                        # print(
                        #     f'[12/13] [open_login] widget.currentIndex() : {widget.currentIndex()}')
                        widget.setCurrentIndex(PROGRESS_PAGE_NO)

                    # (비)활성, 유효 기간 지남
                    elif db_connect.check_activate(user_id) == 1 and db_connect.check_expired_date(user_id) == False:
                        db_connect.update_deactivate_by_expired_date(user_id)
                        win = SubWindow(12)
                        r = win.showModal()
                    # 데모, 유효 기간 안지남
                    elif db_connect.check_activate(user_id) == 2 and db_connect.check_expired_date(user_id) == True:
                        LOGIN_STATUS = 1  # 데모/ 유효기간 남음
                        db_connect.update_activate_by_expired_date(user_id)
                        # print('데모, 유효 기간 안지남')
                        # win = SubWindow(11)
                        # r = win.showModal()
                        # if r == 1:
                        profile = db_connect.get_user_info(user_id)
                        # print(f'[12/22] Saved sprofile : {profile}')
                        profile_file = open('profile.pkl', 'wb')
                        profile_user_name = profile["email"]
                        # print(f'[12/22] Saved profile_user_name : {profile_user_name}')
                        pickle.dump(profile, profile_file)
                        profile_file.close()

                        USER_EMAIL = user_id

                        lastest_login_date = datetime.today().strftime('%Y-%m-%d')
                        # print(f'lastest_login_date : {lastest_login_date}')
                        db_connect.update_latest_login_date(
                            user_id, lastest_login_date)
                        db_connect.insert_log_data(
                            user_id, lastest_login_date)
                        # win = SubWindow(3)
                        # r = win.showModal()
                        # print(
                        #     f'[12/13] [open_login] widget.currentIndex() : {widget.currentIndex()}')
                        widget.setCurrentIndex(PROGRESS_PAGE_NO)
                    # 데모, 유효 기간 지남
                    elif db_connect.check_activate(user_id) == 2 and db_connect.check_expired_date(user_id) == False:
                        # print('데모, 유효 기간 지남')
                        db_connect.update_deactivate_by_expired_date(user_id)
                        win = SubWindow(13)
                        r = win.showModal()
                    else:
                        db_connect.update_deactivate_by_expired_date(user_id)
                        win = SubWindow(14)
                        r = win.showModal()
            else:
                win = SubWindow(2)
                r = win.showModal()

    def open_register(self):
        # print(
        #     f'[12/13] [open_register] widget.currentIndex() : {widget.currentIndex()}')
        widget.setCurrentIndex(REGISTER_PAGE_NO)


class RegisterClass(QDialog):
    global duplicated_btn_checked
    unique_email = False
    company_name_list = []

    duplicated_btn_checked = False
    def __init__(self):
        super().__init__()
        # loadUi("register.ui", self)
        register_ui_file = resource_path("register.ui")
        loadUi(register_ui_file, self)
        logo_pixmap = QPixmap("logo_lg.png")
        self.label_logo.setPixmap(QPixmap(logo_pixmap))
        logo_pixmap = QPixmap("logo_lg.png")
        self.label_logo.setPixmap(QPixmap(logo_pixmap))
        self.email_check_BTN.clicked.connect(self.check_duplicate_email)
        self.confirmBTN.clicked.connect(self.insert_db_account_info)
        self.cancelBTN.clicked.connect(self.cancel_register)
        self.licence_type_combo.addItem('Floating')
        self.licence_type_combo.addItem('Nodelock')
        self.company_name_list = db_connect.get_company_name()
        for c_name in self.company_name_list:
            self.comany_name_combo.addItem(c_name)

        self.radioButton_1.setHidden(True)
        self.radioButton_2.setHidden(True)
        self.radioButton_3.setHidden(True)
        self.radioButton_4.setHidden(True)
        self.radioButton_5.setHidden(True)
        self.radioButton_6.setHidden(True)

        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        # print(f'[12/13] news_list : {news_list_info}')
        # print(f'[12/13] news_list_counter : {news_list_counter}')

        counter = 0
        if counter == 0 and counter < news_list_counter:
            self.radioButton_1.setHidden(False)
            self.radioButton_1.setText(news_list_info[counter][0].lstrip())
            self.radioButton_1.clicked.connect(self.open_webbrowser_0)
            counter += 1
        else:
            self.radioButton_1.setHidden(True)

        if counter == 1 and counter < news_list_counter:
            self.radioButton_2.setHidden(False)
            self.radioButton_2.setText(news_list_info[counter][0].lstrip())
            self.radioButton_2.clicked.connect(self.open_webbrowser_1)
            counter += 1
        else:
            self.radioButton_2.setHidden(True)

        if counter == 2 and counter < news_list_counter:
            self.radioButton_3.setHidden(False)
            self.radioButton_3.setText(news_list_info[counter][0].lstrip())
            self.radioButton_3.clicked.connect(self.open_webbrowser_2)
            counter += 1
        else:
            self.radioButton_3.setHidden(True)

        if counter == 3 and counter < news_list_counter:
            self.radioButton_4.setHidden(False)
            self.radioButton_4.setText(news_list_info[counter][0].lstrip())
            self.radioButton_4.clicked.connect(self.open_webbrowser_3)
            counter += 1
        else:
            self.radioButton_4.setHidden(True)

        if counter == 4 and counter < news_list_counter:
            self.radioButton_5.setHidden(False)
            self.radioButton_5.setText(news_list_info[counter][0].lstrip())
            self.radioButton_5.clicked.connect(self.open_webbrowser_4)
            counter += 1
        else:
            self.radioButton_5.setHidden(True)

        if counter == 5 and counter < news_list_counter:
            self.radioButton_6.setHidden(False)
            self.radioButton_6.setText(news_list_info[counter][0].lstrip())
            self.radioButton_6.clicked.connect(self.open_webbrowser_5)
            counter += 1
        else:
            self.radioButton_6.setHidden(True)

    def cancel_register(self):
        widget.setCurrentIndex(LOGIN_PAGE_NO)

    def check_duplicate_email(self):
        global duplicated_btn_checked
        email_id = self.email_edit.text()
        if db_connect.check_duplicate_account(email_id) == False:
            win = SubWindow(4)
            r = win.showModal()

            self.unique_email = False
        else:
            win = SubWindow(5)
            r = win.showModal()

            self.unique_email = True
        duplicated_btn_checked = True

    def insert_db_account_info(self):
        status = False
        user_name = self.name_edit.text()
        user_email = self.email_edit.text()
        passwd = self.passwd_edit.text()
        passwd_check = self.passwd_check_edit.text()
        contact_info = self.contact_edit.text()
        serial_no_info = self.serial_no_edit.text()
        licence_type_info = self.licence_type_combo.currentText()
        company_name_info = self.comany_name_combo.currentText()
        team_name = self.team_name_edit.text()

        if duplicated_btn_checked == True:
            if len(user_name) > 0 and len(user_email) > 0 and len(passwd) and len(passwd_check) and len(contact_info) and len(serial_no_info) and len(licence_type_info) and len(company_name_info) and len(team_name):
                if passwd == passwd_check:
                    status = db_connect.insert_user_account(
                        user_name, user_email, passwd, contact_info, serial_no_info, licence_type_info, company_name_info, team_name)

                    if status == True:
                        win = SubWindow(6)
                        r = win.showModal()
                        # print(
                        #     f'[12/13] [insert_db_account_info] widget.currentIndex() : {widget.currentIndex()}')
                        # widget.setCurrentIndex(widget.currentIndex()-1)
                        widget.setCurrentIndex(0)

                        # send new register @@2022.01.13
                        target_email = "tasking@hancomit.com"
                        register_email = gmail_sender(
                            "HancomTasking@gmail.com", target_email, "Tasking123!")
                        email_body = 'User name : ' + user_name + '\n'
                        email_body += 'User email : ' + user_email + '\n'
                        email_body += 'Contact info : ' + contact_info + '\n'
                        email_body += 'Serial No. : ' + serial_no_info + '\n'
                        email_body += 'License type : ' + licence_type_info + '\n'
                        email_body += 'Company name : ' + company_name_info + '\n'
                        email_body += 'Team name : ' + team_name + '\n'
                        register_email.msg_get("New Registration", email_body)
                        register_email.smtp_connect_send()
                        register_email.smtp_disconect()

                    else:
                        win = SubWindow(7)
                        r = win.showModal()
                else:
                    win = SubWindow(8)
                    r = win.showModal()
            else:
                win = SubWindow(9)
                r = win.showModal()
        else:
            win = SubWindow(15)
            r = win.showModal()

    def open_webbrowser_0(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        print(f'[12/15] group box clicked')
        url = news_list_info[0][1]
        webbrowser.open(url)

    def open_webbrowser_1(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[1][1]
        webbrowser.open(url)

    def open_webbrowser_2(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[2][1]
        webbrowser.open(url)

    def open_webbrowser_3(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[3][1]
        webbrowser.open(url)

    def open_webbrowser_4(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[4][1]
        webbrowser.open(url)

    def open_webbrowser_5(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[5][1]
        webbrowser.open(url)


class ProcessClass(QDialog):

    def __init__(self):
        global USER_EMAIL
        global LOGIN_STATUS

        super().__init__()
        # loadUi("process.ui", self)
        process_ui_file = resource_path("process.ui")
        loadUi(process_ui_file, self)
        logo_pixmap = QPixmap(":/icon/parser_title.png")
        self.label_title.setPixmap(QPixmap(logo_pixmap))

        logo_pixmap = QPixmap(":/icon/logo_sm.png")
        self.label_logo.setPixmap(QPixmap(logo_pixmap))

        user_logo_pixmap = QPixmap(":/icon/icon_T.png")
        self.label_user_logo.setPixmap(QPixmap(user_logo_pixmap))

        label_upload_logo_sm_pixmap = QPixmap(":/icon/icon_group_sm.png")
        self.label_upload_logo_sm.setPixmap(
            QPixmap(label_upload_logo_sm_pixmap))
        label_upload_logo_lg_pixmap = QPixmap(":/icon/icon_group_lg.png")

        self.label_upload_logo_lg.setPixmap(
            QPixmap(label_upload_logo_lg_pixmap))

        self.timer = QBasicTimer()
        self.step = 0

        self.file_upload_BTN.clicked.connect(self.file_upload_dlg_showDialog)
        self.generating_BTN.clicked.connect(self.generating_process)
        self.logout_BTN.clicked.connect(self.logout_process)

        if os.path.isfile('profile.pkl'):
            profile_file = open("profile.pkl", "rb")
            user_profile = pickle.load(profile_file)
            profile_user_name = user_profile['email']
            # print(f'[12/22] Load profile_user_name : {profile_user_name}')
            profile_file.close()
        else:
            user_profile = {"email": '', "contact": '', "serial_no": '',
                            "licence_type": '', "company_name": '', "tema_name": ''}

        profile_user_name = user_profile['email']
        # print(f"[12/30] user_profile['email'] : {profile_user_name}")
        # self.label_user_name.setText(user_profile['email'])

        LOGIN_STATUS = self.get_buttom_str_status(profile_user_name)
        # print(f'[01/27] LOGIN_STATUS : {LOGIN_STATUS}')
        if LOGIN_STATUS == 1:
            self.label_expired_info.setHidden(False)
            str_demo_date, remain_days = db_connect.get_demo_date(
                profile_user_name)
            str_info = "데모 기간은 " + str_demo_date + \
                "까지 입니다. 데모 기간이 " + remain_days + "일 남았습니다."
            self.label_expired_info.setText(str_info)
        elif LOGIN_STATUS == 2:
            self.label_expired_info.setHidden(False)
            str_expired_date, remain_days = db_connect.get_expired_date(
                profile_user_name)
            str_info = "유지 보수 기간은 " + str_expired_date + \
                "까지 입니다. 유지 보수 기간이 " + remain_days + "일 남았습니다."
            self.label_expired_info.setText(str_info)
        else:
            self.label_expired_info.setHidden(False)

        self.radioButton_1.setHidden(True)
        self.radioButton_2.setHidden(True)
        self.radioButton_3.setHidden(True)
        self.radioButton_4.setHidden(True)
        self.radioButton_5.setHidden(True)
        self.radioButton_6.setHidden(True)

        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        # print(f'[12/13] news_list : {news_list_info}')
        # print(f'[12/13] news_list_counter : {news_list_counter}')

        counter = 0
        if counter == 0 and counter < news_list_counter:
            self.radioButton_1.setHidden(False)
            self.radioButton_1.setText(news_list_info[counter][0].lstrip())
            self.radioButton_1.clicked.connect(self.open_webbrowser_0)
            counter += 1
        else:
            self.radioButton_1.setHidden(True)

        if counter == 1 and counter < news_list_counter:
            self.radioButton_2.setHidden(False)
            self.radioButton_2.setText(news_list_info[counter][0].lstrip())
            self.radioButton_2.clicked.connect(self.open_webbrowser_1)
            counter += 1
        else:
            self.radioButton_2.setHidden(True)

        if counter == 2 and counter < news_list_counter:
            self.radioButton_3.setHidden(False)
            self.radioButton_3.setText(news_list_info[counter][0].lstrip())
            self.radioButton_3.clicked.connect(self.open_webbrowser_2)
            counter += 1
        else:
            self.radioButton_3.setHidden(True)

        if counter == 3 and counter < news_list_counter:
            self.radioButton_4.setHidden(False)
            self.radioButton_4.setText(news_list_info[counter][0].lstrip())
            self.radioButton_4.clicked.connect(self.open_webbrowser_3)
            counter += 1
        else:
            self.radioButton_4.setHidden(True)

        if counter == 4 and counter < news_list_counter:
            self.radioButton_5.setHidden(False)
            self.radioButton_5.setText(news_list_info[counter][0].lstrip())
            self.radioButton_5.clicked.connect(self.open_webbrowser_4)
            counter += 1
        else:
            self.radioButton_5.setHidden(True)

        if counter == 5 and counter < news_list_counter:
            self.radioButton_6.setHidden(False)
            self.radioButton_6.setText(news_list_info[counter][0].lstrip())
            self.radioButton_6.clicked.connect(self.open_webbrowser_5)
            counter += 1
        else:
            self.radioButton_6.setHidden(True)

    def get_buttom_str_status(self, user_id):
        if db_connect.check_demo_status(user_id) == True:
            return 1
        else:
            if db_connect.check_activate(user_id) == 1 and db_connect.check_expired_date(user_id) == True:
                return 2
            elif db_connect.check_activate(user_id) == 2 and db_connect.check_expired_date(user_id) == True:
                return 1

        return 0

    def open_webbrowser_0(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        print(f'[12/15] group box clicked')
        url = news_list_info[0][1]
        webbrowser.open(url)

    def open_webbrowser_1(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[1][1]
        webbrowser.open(url)

    def open_webbrowser_2(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[2][1]
        webbrowser.open(url)

    def open_webbrowser_3(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[3][1]
        webbrowser.open(url)

    def open_webbrowser_4(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[4][1]
        webbrowser.open(url)

    def open_webbrowser_5(self):
        news_list = db_connect.get_news()

        news_list_counter = len(news_list)
        news_list_info = news_list

        url = news_list_info[5][1]
        webbrowser.open(url)

    def logout_process(self):
        # sys.exit(app.exec_())
        widget.setCurrentIndex(LOGIN_PAGE_NO)

    def file_upload_dlg_showDialog(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            self, self.tr('Open File'), './', self.tr('Map file (*.map)'))

        self.file_upload_edit.setText(filename[0])

    def generating_process(self):
        print("Mapfile parsing is in progress…. ")
        print("Please wait ... ")  

        if self.timer.isActive():
            self.timer.stop()
            # self.btn.setText('Start')
        else:
            self.step = 0
            self.timer.start(100, self)

        if self.file_upload_edit.text != '':

            to_parsring_file_name = self.file_upload_edit.text()
            # print(f'(generating_BTN) to_parsring_file_name : {to_parsring_file_name}')
            map_parser.parser_main(to_parsring_file_name)

            if os.path.isfile('profile.pkl'):
                profile_file = open("profile.pkl", "rb")
                user_profile = pickle.load(profile_file)
                profile_file.close()
            else:
                user_profile = {"email": '', "contact": '', "serial_no": '',
                                "licence_type": '', "company_name": '', "tema_name": ''}
            user_id = user_profile['email']
            # print('Connecting Server ...')
            str_execution_counter = db_connect.get_execution_counter(
                user_id)
            int_execution_counter = int(str_execution_counter)
            int_execution_counter += 1
            db_connect.update_execution_counter(
                user_id, int_execution_counter)
        else:
            print('map file is NOT selected ...')

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            win = SubWindow(10)
            r = win.showModal()
            self.progressBar.setValue(0)
            map_parser.init_dir()

            return

        self.step = self.step + 1
        self.progressBar.setValue(self.step)


if __name__ == "__main__":

    if not os.path.isfile('./profile.pkl'):
        user_profile = {"email": '', "pass": '', "contact": '', "serial_no": '',
                        "licence_type": '', "company_name": '', "tema_name": ''}
        profile_file = open('profile.pkl', 'wb')
        pickle.dump(user_profile, profile_file)
        profile_file.close()

    if not os.path.isfile('./use_profile.pkl'):
        use_profile_file = open('use_profile.pkl', 'wb')
        pickle.dump(0, use_profile_file)
        use_profile_file.close()

    # QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv)

    # 화면 전환용 Widget 설정
    widget = QtWidgets.QStackedWidget()

    # 레이아웃 인스턴스 생성
    mainWindow = MainWindow()
    # mainWindow.setWindowTitle('MapParser')
    processWindow = ProcessClass()
    registerWindow = RegisterClass()

    # Widget 추가
    widget.addWidget(mainWindow)
    widget.addWidget(processWindow)
    widget.addWidget(registerWindow)

    # 프로그램 화면을 보여주는 코드
    # widget.setFixedHeight(275)
    # widget.setFixedWidth(390)
    widget.setFixedWidth(1109)
    widget.setFixedHeight(897)
    widget.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
