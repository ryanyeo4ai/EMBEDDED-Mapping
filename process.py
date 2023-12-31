# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\process.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


# import icon_T_rc
from PyQt5 import QtCore, QtGui, QtWidgets


class Process_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1184, 914)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(40, 30, 1071, 121))
        self.groupBox.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox.setObjectName("groupBox")
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setGeometry(QtCore.QRect(20, 30, 401, 61))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_10.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(790, 20, 101, 91))
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap(":/icon/icon_T.png"))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(890, 60, 161, 41))
        self.label_2.setStyleSheet("background-color: rgb(0, 0, 255);\n"
                                   "color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(890, 20, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(40, 160, 1071, 471))
        self.groupBox_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_2.setObjectName("groupBox_2")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(40, 40, 41, 61))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap(":/icon/icon_group.png"))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setGeometry(QtCore.QRect(90, 60, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_5.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setGeometry(QtCore.QRect(450, 150, 111, 91))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap(":/icon/icon_large_group.png"))
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.groupBox_3 = QtWidgets.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(50, 110, 961, 251))
        self.groupBox_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_3.setFlat(False)
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setGeometry(QtCore.QRect(30, 150, 891, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(0, 0, 0);")
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.groupBox_3)
        self.label_8.setGeometry(QtCore.QRect(140, 190, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Adobe Devanagari")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setStyleSheet("color: rgb(0, 0, 255);")
        self.label_8.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox_3)
        self.lineEdit.setGeometry(QtCore.QRect(260, 190, 551, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setGeometry(QtCore.QRect(50, 390, 161, 41))
        self.label_9.setStyleSheet("background-color: rgb(0, 0, 255);\n"
                                   "color: rgb(255, 255, 255);")
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.checkBox = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox.setGeometry(QtCore.QRect(240, 400, 116, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox_2)
        self.checkBox_2.setGeometry(QtCore.QRect(310, 400, 116, 31))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.progressBar = QtWidgets.QProgressBar(self.groupBox_2)
        self.progressBar.setGeometry(QtCore.QRect(420, 400, 581, 31))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.groupBox_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.label_9.raise_()
        self.checkBox.raise_()
        self.checkBox_2.raise_()
        self.progressBar.raise_()
        self.groupBox_4 = QtWidgets.QGroupBox(Dialog)
        self.groupBox_4.setGeometry(QtCore.QRect(40, 680, 1061, 231))
        self.groupBox_4.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_12 = QtWidgets.QLabel(self.groupBox_4)
        self.label_12.setGeometry(QtCore.QRect(290, 40, 371, 41))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.label_12.setFont(font)
        self.label_12.setStyleSheet("color: rgb(0, 170, 0);")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.groupBox_4)
        self.label_13.setGeometry(QtCore.QRect(30, 100, 391, 31))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self.groupBox_4)
        self.label_14.setGeometry(QtCore.QRect(30, 150, 391, 31))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self.groupBox_4)
        self.label_15.setGeometry(QtCore.QRect(30, 200, 391, 31))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self.groupBox_4)
        self.label_16.setGeometry(QtCore.QRect(520, 150, 391, 31))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self.groupBox_4)
        self.label_17.setGeometry(QtCore.QRect(520, 200, 391, 31))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(self.groupBox_4)
        self.label_18.setGeometry(QtCore.QRect(520, 100, 391, 31))
        self.label_18.setObjectName("label_18")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(500, 640, 141, 31))
        self.label_11.setText("")
        self.label_11.setPixmap(QtGui.QPixmap(":/icon/logo_sm.png"))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.groupBox.setTitle(_translate("Dialog", "GroupBox"))
        self.label_10.setText(_translate("Dialog", "TASKING MAP Parser"))
        self.label_2.setText(_translate("Dialog", "로그아웃"))
        self.label_3.setText(_translate("Dialog", "김태스 (ADS팀)"))
        self.groupBox_2.setTitle(_translate("Dialog", "GroupBox"))
        self.label_5.setText(_translate("Dialog", "파일 업로드"))
        self.groupBox_3.setTitle(_translate("Dialog", "GroupBox"))
        self.label_7.setText(_translate(
            "Dialog", "변환할 문서 혹은 폴더를 올려놓거나, 이곳을 클릭하여 파일을 선택하세요."))
        self.label_8.setText(_translate("Dialog", "파일 업로드"))
        self.label_9.setText(_translate("Dialog", "레포트 생성"))
        self.checkBox.setText(_translate("Dialog", "pdf"))
        self.checkBox_2.setText(_translate("Dialog", "csv"))
        self.groupBox_4.setTitle(_translate("Dialog", "GroupBox"))
        self.label_12.setText(_translate("Dialog", "TASKING News."))
        self.label_13.setText(_translate(
            "Dialog", "[TASKING 컴파일러]  HEX 파일의 구조 Part 2"))
        self.label_14.setText(_translate(
            "Dialog", "[TASKING 컴파일러]  HEX 파일의 구조 Part 2"))
        self.label_15.setText(_translate(
            "Dialog", "[TASKING 컴파일러]  HEX 파일의 구조 Part 2"))
        self.label_16.setText(_translate(
            "Dialog", "[TASKING 업데이트] 새로운 소식 확인해보세요"))
        self.label_17.setText(_translate(
            "Dialog", "[TASKING 업데이트] 새로운 소식 확인해보세요"))
        self.label_18.setText(_translate(
            "Dialog", "[TASKING 업데이트] 새로운 소식 확인해보세요"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    process_ui = Process_Dialog()
    process_ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
