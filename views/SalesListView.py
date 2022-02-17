# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 20:37:06 2021

@author: kuromi
"""

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
from PyQt5.QtGui import *

dialog_class = uic.loadUiType("./UI/SalesList.ui")[0]

class SalesList(QDialog, dialog_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #self.can.clicked.connect(QCoreApplication.instance().quit)
        self.orderTable.setEditTriggers(QAbstractItemView.NoEditTriggers)

        if(self.card_btn.isEnabled()):
            self.card_btn.setEnabled(False)
        else:
            self.cash_btn.setEnabled(True)

    def cardSelect(self):
         self.getMoney.setEnabled(False)
         self.card_btn.setEnabled(False)
         self.cash_btn.setEnabled(True)
         
    def cashSelect(self):
         self.getMoney.setEnabled(True)
         self.card_btn.setEnabled(True)
         self.cash_btn.setEnabled(False)
         
    def selectionChanged(self):
        print("Selected changed: ")
        

    def ListUpdate(self,TableMenuList):
        self.sellList.clear()
        for Menu in TableMenuList:       
            self.sellList.addItem(Menu.menuName)


            
    def OrderUpdate(self,TableOrderList): # [  [상품명, 수량, 가격] , [상품명, 수량, 가격] ]
        #self.OrderTable.clearContents()
        while self.orderTable.rowCount() > 0 :
                self.orderTable.removeRow(0)
        
        self.orderTable.setRowCount(len(TableOrderList))   
        
        row = 0
        for Menu in TableOrderList:       #여기서 저 테이블 칸에다가 적절하게 분산해서 데이터 저장해야함
            self.orderTable.setItem(row,0, QTableWidgetItem(Menu[0]))
            self.orderTable.setItem(row,1, QTableWidgetItem(str(Menu[1])))
            self.orderTable.setItem(row,2, QTableWidgetItem(str(Menu[1] * Menu[2])))
            row = row + 1
    
    def clear(self): #초기화 시, 추가한 만큼 다시 재고 채워 줘야함 -> model에서 해결. 완
        while self.orderTable.rowCount() > 0 :
                self.orderTable.removeRow(0)
        
        self.totalPrice.setText('0')
        self.changeMoney.setText('0')


        
    def Areceipt(self, time, orderInfo, cgetmoney): # 메뉴명이 나옴 True
        if self.card_btn.isEnabled(): # 카드가 활성화 되어있는 경우 -> 즉, 현금결제를 선택한 상황
            self._receipt = ReciptWidget('현금결제.png',time,orderInfo,True,'cash',cgetmoney)
            self._receipt.show()

            
        
        else : # 카드 결제
            self._receipt = ReciptWidget('카드결제.png',time,orderInfo,True,'card',cgetmoney)
            self._receipt.show()
         
        
        
    def Breceipt(self, time, orderInfo ,cgetmoney): # 메뉴명 비공개 False
        if self.card_btn.isEnabled(): # 카드가 활성화 되어있는 경우 -> 즉, 현금결제를 선택한 상황
            self._receipt = ReciptWidget('현금결제.png',time,orderInfo,False,'cash',cgetmoney)
            self._receipt.show()            
        
        else : # 카드 결제
            self._receipt = ReciptWidget('카드결제.png',time,orderInfo,False,'card',cgetmoney)
            self._receipt.show()    
            
        

        
class Label(QLabel):
    def __init__(self,__dir,time,orderInfo,ismenu,pay,cgetmoney):

        self._time = time
        self._orderInfo = orderInfo
        self._ismenu = ismenu
        self._pay = pay
        self._dir = __dir
        self._total = 0
        self._currentgetmoney = cgetmoney
        super().__init__()

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)

        self.image  = QImage(self._dir)
        qp.drawImage(QPoint(), self.image)

        pen = QPen(Qt.black)
        pen.setWidth(2)
        qp.setPen(pen)        

        font = QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(10)
        qp.setFont(font)
        
        for order in self._orderInfo:
            self._total = self._total + (order[1] * order[2])
            
            
        if self._ismenu :        # A타입
            x = 60
            y = 200
            for order in self._orderInfo:    
                qp.drawText(x, y, order[0])
                qp.drawText(x+133, y, str(order[2]))
                qp.drawText(x+240, y, str(order[1]))
                qp.drawText(x+340, y, str(order[1] * order[2]))
                y += 30
                    
        
        else : # B 타입
            pass
        
        
        if self._pay == 'card' :
            x = 400
            y = 565
            qp.drawText(x, y, str(self._total))
            
            y = 605
            qp.drawText(x, y, str(self._total))
        elif self._pay == 'cash':
            x = 400
            y = 528
            qp.drawText(x, y, str(self._total))
            y = 565
            _changeMoney = self._currentgetmoney - self._total
            qp.drawText(x, y, str(self._currentgetmoney))
            y = 605
            qp.drawText(x, y, str(_changeMoney))           
        
        self._total = 0
        x = 380
        y = 120
        qp.drawText(x, y, self._time)   
        qp.end()


class ReciptWidget(QWidget):
    def __init__(self,__dir,time,orderInfo,ismenu,pay,cgetmoney):
        super().__init__()
        self.setGeometry(50, 50, 580, 800)
        self.setWindowTitle("ANOPOS 영수증")

        self.label = Label(__dir,time,orderInfo,ismenu,pay,cgetmoney) 

        self.grid = QGridLayout()
        self.grid.addWidget(self.label)
        self.setLayout(self.grid)

        