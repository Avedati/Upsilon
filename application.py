from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 
from urllib.request import urlopen
from parser import Parser

# https://pythonspot.com
class Application(QWidget):

    def __init__(self):
        super().__init__()
        self.content = ['']
        self.text = None
        self.labl = None
        self.pos = 0
        self.title = 'Simple Web Scraper - Written in Python'
        self.left = 10
        self.top = 10
        self.width = 840
        self.height = 680
        self.initUI()

    def btn_1_pressed(self):
        if len(self.content) > 0:
            self.pos -= 1
            if self.pos < 0:
                self.pos = len(self.content) - 1

            self.labl.setText(self.content[self.pos])

    def btn_2_pressed(self):
        if len(self.content) > 0:
            self.pos = (self.pos + 1) % len(self.content)
            self.labl.setText(self.content[self.pos])

    def return_typed(self):
        url = self.text.text()
        page = urlopen(url)
        content = str(page.read())
        parser = Parser(content)
        self.content = parser.parse()

        if len(self.content) == 0:
            self.content = ['']

        self.labl.setText(self.content[self.pos])

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.text = QLineEdit(self)
        self.text.move(20, 20)
        self.text.resize(800, 40)
        self.text.setFont(QFont('Anonymous Pro', 16))
        self.text.returnPressed.connect(self.return_typed)

        btn1 = QPushButton('<', self)
        btn1.setFont(QFont("Anonymous Pro", 32))
        btn1.setToolTip('Previous string')
        btn1.resize(200, 100)
        btn1.move(40, 390)
        btn1.clicked.connect(self.btn_1_pressed)

        self.labl = QLabel(self.content[self.pos], self)
        self.labl.setFont(QFont("Anonymous Pro", 16))
        self.labl.setToolTip('')
        self.labl.setAlignment(Qt.AlignCenter)
        self.labl.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.labl.setWordWrap(True)
        self.labl.resize(360, 300)
        self.labl.move(240, 290)

        btn2 = QPushButton('>', self)
        btn2.setFont(QFont("Anonymous Pro", 32))
        btn2.setToolTip('Next string')
        btn2.resize(200, 100)
        btn2.move(600, 390)
        btn2.clicked.connect(self.btn_2_pressed)

        self.show()
