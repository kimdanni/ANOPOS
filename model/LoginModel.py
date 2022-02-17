# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 14:14:08 2021

@author: kuromi
"""
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from model.AccountManager import *

class LoginModel:
    def __init__(self):
        self.userId = ""
        self.password = ""
        self.IsLoginSuccess = False
        AccManager = AccountManager()
        
    def verify_password(self):
        AccManager = AccountManager()
        print(self.userId, self.password, "model test")
        self.IsLoginSuccess = AccManager.login(self.userId, self.password)
        return self.IsLoginSuccess
    
    def AddAccount(self):
        AccManager = AccountManager()
        AccManager.AddAccount(self.userId, self.password, False)
    
    def verify_ID(self):
        AccManager = AccountManager()
        return AccManager.IsSameID(self.userId)