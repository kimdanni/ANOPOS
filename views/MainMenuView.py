# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 17:13:41 2021

@author: kuromi
"""

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("./UI/MainWindow.ui")[0]

class MainMenuView(QMainWindow, form_class):
    def __init__(self):
        super().__init__()