import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic

dialog_class = uic.loadUiType("./UI/signin.ui")[0]

class SigninView(QDialog, dialog_class):
    def __init__(self):
        super().__init__()
        self.userId = ""
        self.password = ""
        self.setupUi(self)
    def userInfo(self):
        self.userId = self.Signin_IDEdit.text()
        self.password = self.Signin_PWEdit.text()
        
    def clear(self):
        self.Signin_IDEdit.setText("ID")
        self.Signin_PWEdit.setText("PassWord")
        
    def checkedId(self):
        self.OKBtn.setEnabled(True)
        self.confirmLabel.setText("U CAN USE THIS ID")
        
    def showError(self):
        self.OKBtn.setEnabled(False)
        self.confirmLabel.setText("LOGIN FAILED")
    
    def showSuccess(self):
        self.OKBtn.setEnabled(False)
        self.confirmLabel.setText("Account Registered!")