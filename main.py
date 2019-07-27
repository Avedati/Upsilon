# https://stackoverflow.com/questions/1843424/get-webpage-contents-with-python
import sys
from PyQt5.QtWidgets import QApplication
from application import Application

if __name__ == '__main__':
    # https://pythonspot.com
    app = QApplication(sys.argv)
    ex = Application()
    sys.exit(app.exec_())
