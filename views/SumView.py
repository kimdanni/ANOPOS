#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 22:37:49 2021

@author: mymelo
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic


class SalesList(QDialog, dialog_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# ???