import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
import db_connect


class SubWindow(QDialog):
    def __init__(self, flag):
        super().__init__()
        self.initUI(flag)

    def initUI(self, flag):
        if flag == 3:
            self.setWindowTitle('로그인 성공')
        elif flag == 4:
            self.setWindowTitle('회원 가입 오류')
        elif flag == 5 or flag == 6:
            self.setWindowTitle('정상 회원 가입')
        elif flag == 7 or flag == 8:
            self.setWindowTitle('회원 가입 오류')
        elif flag == 10:
            self.setWindowTitle('파싱')
        elif flag == 11:
            self.setWindowTitle('프로그램 정보')
        elif flag == 12:
            self.setWindowTitle('유지보수 정보')
        elif flag == 13:
            self.setWindowTitle('비활성화 정보')
        elif flag == 14:
            self.setWindowTitle('비활성화 정보')
        elif flag == 15:
            self.setWindowTitle('회원 가입 오류')
        elif flag == 100:
            self.setWindowTitle('업그레이드')
        elif flag == 101:
            self.setWindowTitle('다운로드')
        else:
            self.setWindowTitle('로그인 오류')

        # self.setGeometry(100, 100, 200, 100)
        layout = QVBoxLayout()
        layout.addStretch(1)
        label_1 = QLabel()
        if flag == 1 or flag == 2:
            label_1.setText('등록한 이메일의 비밀번호가 틀립니다')
        elif flag == 3:
            label_1.setText('이메일과 비밀번호가 일치합니다.')
        elif flag == 4:
            label_1.setText('등록한 이메일이 존재합니다.')
        elif flag == 5:
            label_1.setText('사용 가능한 이메일입니다.')
        elif flag == 6:
            label_1.setText('회원 가입이 정상적으로 완료됐습니다.')
        elif flag == 7:
            label_1.setText('회원 가입에 문제가 발생했습니다. ')
        elif flag == 8:
            label_1.setText('비밀번호가 일치하지 않습니다. ')
        label_2 = QLabel()

        if flag == 1 or flag == 2:
            label_2.setText('올바른 이메일과 비밀번호를 입력해주세요.')
        elif flag == 4 or flag == 7:
            label_2.setText('tasking@hancomit.com으로 문의해주세요.')
        elif flag == 8:
            label_2.setText('비밀번호를 정확하게 입력해주세요.')
        elif flag == 9:
            label_2.setText('모든 정보를 입력해주세요.')
        elif flag == 10:
            label_2.setText('맵 파일의 파싱이 끝났습니다.')
        elif flag == 11:
            label_2.setText(
                'Demo 기간(30일)동안 무상으로 사용할 수 있습니다.\n Demo 기간 이후 유지보수 기간이 유효한 경우 사용 가능합니다.')
        elif flag == 12:
            label_2.setText('유지 보수 기간이 종료되었습니다.')
        elif flag == 13:
            label_2.setText(
                'Demo 기간(30일)이 경과되어 종료되었습니다. \n 문의 사항이 있으신 경우, tasking@hancomit.com으로 연락주세요')
        elif flag == 14:
            label_2.setText(
                '아이디가 비활성 상태입니다. \n 문의 사항이 있으신 경우, tasking@hancomit.com으로 연락주세요')
        elif flag == 15:
            label_2.setText(
                '아이디의 [중복 확인]을 하지 않았습니다.\n아이디의 [중복 확인] 버튼을 눌러주세요.')
        elif flag == 100:
            db_version = db_connect.get_version_from_db()
            label_2.setText(
                '새 버전 [ ' + db_version + '_mapfile_parser.zip ]이 존재합니다.\n 다운로드할까요?')
        elif flag == 101:
            label_2.setText('다운로드가 완료됐습니다. 새 버전의 압축을 풀고 새로 시작하세요.')
        else:
            label_2.setText('')

        font = label_1.font()
        font.setPointSize(10)
        label_1.setFont(font)
        label_1.setAlignment(Qt.AlignCenter)
        font = label_2.font()
        font.setPointSize(10)
        label_2.setFont(font)
        label_2.setAlignment(Qt.AlignCenter)
        self.label_1 = label_1
        self.label_2 = label_2
        subLayout = QHBoxLayout()

        btnOK = QPushButton("확인")
        btnOK.clicked.connect(self.onOKButtonClicked)
        btnCancel = QPushButton("취소")
        btnCancel.clicked.connect(self.onCancelButtonClicked)

        layout.addWidget(label_1)
        layout.addWidget(label_2)
        subLayout.addWidget(btnOK)
        subLayout.addWidget(btnCancel)
        layout.addLayout(subLayout)
        layout.addStretch(1)
        self.setLayout(layout)

    def onOKButtonClicked(self):
        self.accept()

    def onCancelButtonClicked(self):
        self.reject()

    def showModal(self):
        return super().exec_()
