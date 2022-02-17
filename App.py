# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from controller.MainController import MainController

if __name__ == '__main__':
    app = QApplication(sys.argv)
    c = MainController()
    c.run()
    sys.exit(app.exec_())
