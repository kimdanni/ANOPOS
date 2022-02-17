# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 17:13:41 2021

@author: kuromi
"""

from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("./UI/MainWindow.ui")[0]

class MainWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.userId = ""
        self.password = ""
        self.setupUi(self)

# =============================================================================
#         
#     로그인 화면[0] 관련
#     
# =============================================================================

        
    def userInfo(self):
        self.userId = self.IdEdit.text()
        self.password = self.PassWordEdit.text()
        
    def clear(self):
        self.IdEdit.setText("ID")
        self.PassWordEdit.setText("PassWord")
        
    def showMessage(self):
        self.StatusLabel.setText("LOGIN SUCESS")
        if(self.userId == "admin"): #admin 유저일 때만 signin 가능하도록 구현
            self.SignInBtn.setEnabled(True)
        else:
            self.SignInBtn.setEnabled(False)
        self.GoToMainBtn.setEnabled(True)
        
    def showError(self):
        self.SignInBtn.setEnabled(False)
        self.GoToMainBtn.setEnabled(False)
        self.StatusLabel.setText("LOGIN FAILED")
        
        
        
# =============================================================================
#         
#   영업정보관리 화면[4] 관련
#     
# =============================================================================

    def MenuUpdate(self, MenuList):
        while self.BusinessTable.rowCount() > 0 :
            self.BusinessTable.removeRow(0)
        self.BusinessTable.setRowCount(len(MenuList))
                
        row = 0
        for Menu in MenuList:
            self.BusinessTable.setItem(row, 0, QTableWidgetItem(str(Menu.code)))
            self.BusinessTable.setItem(row, 1, QTableWidgetItem(Menu.category))
            self.BusinessTable.setItem(row, 2, QTableWidgetItem(Menu.menuName))
            self.BusinessTable.setItem(row, 3, QTableWidgetItem(str(Menu.price)))
            self.BusinessTable.setItem(row, 4, QTableWidgetItem(str(Menu.stuck)))
            row += 1


    def RestoreData(self,row,column,data): # 잘못된 값 입력시 되돌리기.
        self.BusinessTable.setItem(row, column, QTableWidgetItem(str(data)))
            
            
    
    def getnewMenu(self):

        _newCode = int(self.newCode.text())
        _newCategory = self.newCategory.text()
        _newPrice = int(self.newPrice.text())
        _newName = self.newName.text()
        _newStuck = int(self.newStuck.text())
        
                        #  코드     카테고리      메뉴명      가격     부자재[리스트]   수량
        newMenuInfo = [ _newCode, _newCategory, _newName, _newPrice, [-1,-1,-1], _newStuck]
        print( _newCode, _newCategory, _newName, _newPrice, [-1,-1,-1], _newStuck)
        return newMenuInfo
        
            
 
    
    
    
    
  
        