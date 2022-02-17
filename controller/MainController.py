# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 14:14:44 2021

@author: kuromi
"""

import pandas as pd
import platform
import numpy as np
import matplotlib.pyplot as plt

import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from model.LoginModel import LoginModel
from model.AccountManager import AccountManager
from views.SigninView import SigninView
from views.MainWindow import MainWindow
from views.SalesListView import SalesList
from model.MenuManager import MenuManager
from model.Table import Table
from model.SalesCSVManager import SalesCSVManager
from model.GenGraph import GenGraph

from PyQt5.QtCore import QTimer, QTime, QDate

from PyQt5.QtGui import QPixmap

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

from matplotlib.backends.backend_qt5agg import FigureCanvas as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import copy
import threading

class MainController(QWidget):
    def __init__(self):
        super(MainController, self).__init__()
        self._currentId = ""
        self.userId = ""
        self.password = ""
        
        self._model = LoginModel()
        self._signinview = SigninView()
        self._mw = MainWindow()
        
        self._salesList = SalesList()
        
        self._setClear = []
        
        self._totalSaleList = []
        
        self._origMenuManager = MenuManager()
        self._menuManager = copy.deepcopy(self._origMenuManager)
        self._TableList = []
        self._origTableList = []
        self._currentTable = ""
        
        self._currentOrderInfo = [123]  # 영수증을 출력할 view로 데이터 넘겨줘야해서..추가했습니다
        self._currentgetmoney = 0
        
        self._timer = QTimer(self)
        self._timer.start()
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.timeout)
        
        self._currentTime = ""
        self._date = ""
       
        for TableNum in range(9):
                self._origTableList.append(Table(self._menuManager.MenuList, TableNum)) #전체 메뉴 리스트와 테이블 번호 전달하여 Table 객체 생성 및 추가
        self._TableList = copy.deepcopy(self._origTableList)  
       
        # error
        self.Errormsg = QMessageBox()
        self.Errormsg.setIcon(QMessageBox.Critical)
        
        
        # for matplot graph
        self.MonthCanvas = None
        self.ProductCanvas = None
        self.UserCanvas = None
        self.TimeCanvas = None
        
        self.forEx = 1
        
        # 달력 관련
        self.year = -1
        self.month = -1
        self.date = -1
        
        self.seller_date = -1
        self.sellermonth = -1
        self.selleryear = -1
        
        self.product_date = -1
        self.productmonth = -1
        self.productyear = -1
        
        self.time_date = -1
        self.timemonth = -1
        self.timeyear = -1
        
        # 달력 이벤트 관련
        self._mw.seller_cal.currentPageChanged.connect(self.SellercalendarPageChanged)
        self._mw.seller_cal.selectionChanged.connect(self.SellercalendarSelectionChanged)
        
        self._mw.product_cal.currentPageChanged.connect(self.ProductcalendarPageChanged)
        self._mw.product_cal.selectionChanged.connect(self.ProductcalendarSelectionChanged)
        
        self._mw.time_cal.currentPageChanged.connect(self.TimecalendarPageChanged)
        self._mw.time_cal.selectionChanged.connect(self.TimecalendarSelectionChanged)
        
        self.initGraph()
        
        self.init()
        
        
        
# =============================================================================
#         
#    현재 시간 관련
#
# =============================================================================
    def timeout(self):
        self.showtimeInfo = ""
        sender = self.sender()
        self._currentTime = QTime.currentTime().toString("hh:mm")
        self._date = QDate.currentDate().toString(Qt.ISODate)
        self.showtimeInfo += self._date
        self.showtimeInfo += " "
        self.showtimeInfo += self._currentTime
        if id(sender) == id(self._timer):
            self._mw.statusBar().showMessage(self.showtimeInfo)
        
    def init(self):
# =============================================================================
#       signin 관련
# =============================================================================
        self._signinview.ConfirmBtn.clicked.connect(self.IDcheck)
        self._signinview.OKBtn.clicked.connect(self.AddAccount)
        

# =============================================================================
#       LOGIN 관련
# =============================================================================
        self._mw.LogInBtn.clicked.connect(self.verify_AnoposUser)
        self._mw.SignInBtn.clicked.connect(self.signinUser)
        self._mw.GoToMainBtn.clicked.connect(lambda : self._mw.stackedWidget.setCurrentIndex(1))
        
        
# =============================================================================
#       REGISGT SALES 관련
# =============================================================================
        self._salesList.reset.clicked.connect(self.clearSalesList)
        self._salesList.sellList.itemClicked.connect(self.OpenSellDialog) # 처음이 0 ? 1??
        self._salesList.getMoney.textChanged.connect(self.ChangeUpdate)   # 받은 금액이 달라질 시
        #self._salesList.TotalPrice.textChanged.connect(self.ChangeUpdate) # 총 결제금액이 달라질 시
        """
        Initialize the integer input field.
        """
        self._salesList.getMoney.setValidator((QIntValidator(self)))        
        
        
# =============================================================================
#       table
# =============================================================================
        self._mw.table1.clicked.connect(lambda : self.SalesList(0))
        self._mw.table2.clicked.connect(lambda : self.SalesList(1))
        self._mw.table3.clicked.connect(lambda : self.SalesList(2))
        self._mw.table4.clicked.connect(lambda : self.SalesList(3))
        self._mw.table5.clicked.connect(lambda : self.SalesList(4))
        self._mw.table6.clicked.connect(lambda : self.SalesList(5))
        self._mw.table7.clicked.connect(lambda : self.SalesList(6))
        self._mw.table8.clicked.connect(lambda : self.SalesList(7))
        self._mw.TakeOut.clicked.connect(lambda : self.SalesList(8))
        self._mw.tbGoToHome.clicked.connect(lambda : self._mw.stackedWidget.setCurrentIndex(1))
        

           
# =============================================================================
#       재고 관리 관련
# =============================================================================
        self._mw.stHomeBtn.clicked.connect(lambda : self._mw.stackedWidget.setCurrentIndex(1))
        
        # 신메뉴 추가
        self._mw.newMenuBtn.clicked.connect(self.newMenuRegist)
        
        # 재고 추가
        self._mw.MenuUpdate(self._menuManager.MenuList)     # CSV에 저장 된 디폴트 메뉴들을 재고관리 화면에 출력. view는 데이터저장 x
        self._mw.BusinessTable.cellClicked.connect(self.GetOrigData)
        self._mw.BusinessTable.cellChanged.connect(self.ChangedSomeData)
# =============================================================================
#       MAIN MENU 관련
# =============================================================================
        self._mw.registSales.clicked.connect(lambda : self._mw.stackedWidget.setCurrentIndex(2))
        self._mw.menageSales.clicked.connect(lambda : self._mw.stackedWidget.setCurrentIndex(4))
        self._mw.salesSt.clicked.connect(lambda : self._mw.stackedWidget.setCurrentIndex(3))
        self._mw.logoutBtn.clicked.connect(lambda : self._mw.stackedWidget.setCurrentIndex(0))
        
# =============================================================================
#       SOLD AND SAVE 관련
# =============================================================================

        self._salesList.soldBtn.clicked.connect(self.SendSoldList)
        self._salesList.card_btn.clicked.connect(self._salesList.cardSelect)
        self._salesList.cash_btn.clicked.connect(self._salesList.cashSelect)
        self._salesList.Atype.clicked.connect(lambda : self._salesList.Areceipt(self.showtimeInfo,self._currentOrderInfo,self._currentgetmoney))
        self._salesList.Btype.clicked.connect(lambda : self._salesList.Breceipt(self.showtimeInfo,self._currentOrderInfo,self._currentgetmoney))    
        

        
# =============================================================================
#     
#       SATISTATIC 관련
#     
# =============================================================================
        ## 메인 화면
        self._mw.main_btn.clicked.connect(self.GenMainInfo)
        self._mw.home_btn.clicked.connect(lambda : self._mw.stackedWidget.setCurrentIndex(1))
    
        ## 월별 통계
#        self._mw.month_st.clicked.connect(self.GenMonthGraph)
        ## 제품별 통계
        self._mw.product_st.clicked.connect(self.GenProductGraph)
        # 사용자 통계
        self._mw.user_st.clicked.connect(self.GenUserGraph)
        # 시간별 통계
        self._mw.time_st.clicked.connect(self.GenTimeGraph)
        
 
# =============================================================================
#     
#     user 관련
#     
# =============================================================================
    def IDcheck(self): #아이디 중복검사
        self._signinview.userInfo()                  #현재 정보 save
        self._model.userId = self._signinview.userId #모델에 아이디 저장
        if self._model.verify_ID():                  #아이디 중복검사
            self._signinview.checkedId()             #아이디 사용가능
        else:
            self._signinview.showError()             #아이디 중복 시, Error 출력 
    
    def AddAccount(self):
        self._signinview.userInfo()
        self._model.userId = self._signinview.userId
        self._model.password = self._signinview.password
        
        self._model.AddAccount()       #permisson 선택 필요 일단은 False..
        self._signinview.clear()
        self._signinview.showSuccess() #회원가입 완료
    
    
    def verify_AnoposUser(self):
        self._mw.userInfo()
        self._model.userId = self._mw.userId
        self._model.password = self._mw.password
        self._mw.clear()
        if self._model.verify_password():
            self._mw.showMessage()
            self._currentId = self._model.userId
        else:
            self._mw.showError()
    
    def signinUser(self):
        self._signinview.show()
        
        
# =============================================================================
#         
#     Sales 관련
#     
# =============================================================================
    def SalesList(self,TableNum):  #SalesList Dialog 화면 출력. 테이블과 / takeout에 따라 다른, 메뉴가 출력되도록 해야함
        print("NOW index {} table".format(TableNum))    
        self._currentTable = TableNum
        self._salesList.ListUpdate(self._TableList[TableNum].TableMenuList)  #1~8 테이블 및 TakeOut에 맞는 메뉴 업데이트(테이블에 메뉴들 등록)
        self._salesList.OrderUpdate(self._TableList[self._currentTable].TableOrderList)
        #self._salesList.OrderUpdate(self._TableList[TableNum].)
        self._salesList.show()
        

    def OpenSellDialog(self): #선택한 메뉴의 인덱스 번호
        
        Menuindex = self._salesList.sellList.currentRow() # 처음이 0 ? 1??
        
        MenuName = self._salesList.sellList.currentItem().text()
        Remain = "" 
        
        for Menu in self._menuManager.MenuList:
            if MenuName == Menu.menuName:
                Remain = Menu.stuck
                break
        
        text, ok = QInputDialog.getText(None, '입력', '잔여 수량 :' + str(Remain) + '\n수량 입력')
        
        if ok:
            try :
                amount = int(text)
                if(amount > Remain):
                    self.Errormsg.setText("재고가 부족합니다!")
                    self.Errormsg.exec_()
                    return
                    
                self._TableList[self._currentTable].AppendOrder(Menuindex, amount)  #현재 열린 테이블에서 선택된 메뉴 index 및 수량 전달
                self._salesList.OrderUpdate(self._TableList[self._currentTable].TableOrderList)
                self._salesList.totalPrice.setText(str(self._TableList[self._currentTable].TotalPrice))
                self.ChangeUpdate()
            
            except ValueError:
              self.Errormsg.setText("숫자만 입력가능합니다!")
              self.Errormsg.exec_()


        
  
    def ChangeUpdate(self):
        salesText = self._salesList.getMoney.text()
        if(salesText == ''):
            salesText = '0'
        Change = int(salesText) - int(self._TableList[self._currentTable].TotalPrice)
        self._salesList.changeMoney.setText(str(Change))
  


    def clearSalesList(self):
        self._TableList[self._currentTable].Reset() # model 에서의 실제 데이터 초기화
        self._salesList.clear()                     # View  에서의 단순 디스플레이 초기화
        self._salesList.totalPrice.setText(str(self._TableList[self._currentTable].TotalPrice))

        
    def run(self):
        self._mw.show()

# =============================================================================
#       SOLD AND SAVE 관련
# =============================================================================
    def SendSoldList(self):
        # 결제 버튼 누를 시, 값들이 전부 초기화 되므로 영수증 출력을 위해서는 저장해 둘 필요가 있음
        self._currentOrderInfo = copy.deepcopy(self._TableList[self._currentTable].TableOrderList)
        self._currentgetmoney = int(self._salesList.getMoney.text())
            
        
        salesCsv = SalesCSVManager()
        #print(self._TableList[self._currentTable].TableOrderList)
        for i in (self._TableList[self._currentTable].TableOrderList):
            i.append(self._date)
            i.append(self._currentTime)
            i.append(self._currentId)
            self._totalSaleList.append(i)
            
        salesCsv.saveCSV(self._totalSaleList, self._signinview.userId) # 잠시 비활성화 좀 해놓을게요 다은님...ㅠㅠㅠ
        
        # 결제가 끝났으므로 화면 초기화 및 주문 리스트 초기화
        self._salesList.clear()
        self._TableList[self._currentTable].orderlistclear()
        self._TableList[self._currentTable].TotalPrice = 0
        

# =============================================================================
#       
#       SAlES 관련
#
# =============================================================================

# 초기화
    def initGraph(self):
        
        g = GenGraph()
        data = g.TotalSales()
        self._mw.main_sell.setText(str(data[0]))
        self._mw.main_count.setText(str(data[1]))
        self._mw.main_seller.setText(str(data[2]))
        
        self.MonthCanvas = FigureCanvas((Figure(figsize=(4,3))))
        self.ProductCanvas = FigureCanvas((Figure(figsize=(4,3))))
        self.UserCanvas = FigureCanvas(Figure(figsize=(4,3)))
        self.TimeCanvas = FigureCanvas((Figure(figsize=(4,3))))
                                       
#        self._mw.month_img.addWidget(self.MonthCanvas)
        self._mw.product_img.addWidget(self.ProductCanvas)
        self._mw.user_img.addWidget(self.UserCanvas)
        self._mw.time_img.addWidget(self.TimeCanvas)
        
        self.month_ax = self.MonthCanvas.figure.subplots()
        self.product_ax = self.ProductCanvas.figure.subplots()
        self.user_ax = self.UserCanvas.figure.subplots()
        self.time_ax = self.TimeCanvas.figure.subplots()
        
    def GenMainInfo(self):
        self._mw.stackedWidget_2.setCurrentIndex(0)
        g = GenGraph()
        data = g.TotalSales()
        self._mw.main_sell.setText(str(data[0]))
        self._mw.main_count.setText(str(data[1]))
        self._mw.main_seller.setText(str(data[2]))
        
    def GenMonthGraph(self):
        self._mw.stackedWidget_2.setCurrentIndex(1)
        self.month_ax.clear()
        g = GenGraph()
        g.GenMonthSt(self.month_ax)
    
    #product
    def GenProductGraph(self):
        self._mw.stackedWidget_2.setCurrentIndex(2)
        self.product_ax.clear()
        g = GenGraph()
        if(self._mw.coin_product.isChecked()):
            g.GenProductSt(self.product_ax, '판매량')
        else:
            g.GenProductSt(self.product_ax, '수량')
    def GenMonthProductGraph(self, year, month):
        self._mw.stackedWidget_2.setCurrentIndex(2)
        self.product_ax.clear()
        g = GenGraph()
        if(self._mw.coin_product.isChecked()):
            g.GenMonthProductSt(self.product_ax, year, month, '판매량')
        else:
            g.GenMonthProductSt(self.product_ax, year, month, '수량')
    def GenYearProductGraph(self, year):
        self._mw.stackedWidget_2.setCurrentIndex(2)
        self.product_ax.clear()
        g = GenGraph()
        if(self._mw.coin_product.isChecked()):
            g.GenYearProductSt(self.product_ax, year, '판매량')
        else:
            g.GenYearProductSt(self.product_ax, year, '수량')
        
    def GenDateProductGraph(self, year, month, date):
        self._mw.stackedWidget_2.setCurrentIndex(2)
        self.product_ax.clear()
        g = GenGraph()
        if(self._mw.coin_product.isChecked()):
           g.GenDateProductSt(self.product_ax, year, month, date, '판매량')
        else:
            g.GenDateProductSt(self.product_ax, month, date, year, '수량')
    
    #user
    def GenUserGraph(self):
        self._mw.stackedWidget_2.setCurrentIndex(3)
        self.user_ax.clear()
        g = GenGraph()
        if(self._mw.coin_seller.isChecked()):
            g.GenUserSt(self.user_ax, '판매량')
        else:
            g.GenUserSt(self.user_ax, '수량')
    
    def GenMonthUserGraph(self, year, month):
        self.user_ax.clear()
        g = GenGraph()
        if(self._mw.coin_seller.isChecked()):
            g.GenMonthUserSt(self.user_ax, year, month, '판매량')
        else:
            g.GenMonthUserSt(self.user_ax, year, month, '수량')
        
    def GenYearUserGraph(self, year):
        self.user_ax.clear()
        g = GenGraph()
        if(self._mw.coin_seller.isChecked()):
            g.GenYearUserSt(self.user_ax, year, '판매량')
        else:
            g.GenYearUserSt(self.user_ax, year, '수량')
    
    def GenDateUserGraph(self, year, month, date):
        self.user_ax.clear()
        g = GenGraph()
        if(self._mw.coin_seller.isChecked()):
            g.GenDateUserSt(self.user_ax, year, month, date, '판매량')
        else:
            g.GenDateUserSt(self.user_ax, year, month, date, '수량')
    
    # time
    def GenTimeGraph(self):
        self._mw.stackedWidget_2.setCurrentIndex(4)
        self.time_ax.clear()
        g = GenGraph()
        if(self._mw.coin_time.isChecked()):
            g.GenTimeSt(self.time_ax, '판매량')
        else:
            g.GenTimeSt(self.time_ax, '수량')
        
    def GenMonthTimeGraph(self, year, month):
        self._mw.stackedWidget_2.setCurrentIndex(4)
        self.time_ax.clear()
        g = GenGraph()
        if(self._mw.coin_time.isChecked()):
            g.GenMonthTimeSt(self.time_ax, year, month, '판매량')
        else:
            g.GenMonthTimeSt(self.time_ax, year, month, '수량')
        
    def GenYearTimeGraph(self, year):
        self._mw.stackedWidget_2.setCurrentIndex(4)
        self.time_ax.clear()
        g = GenGraph()
        if(self._mw.coin_time.isChecked()):
            g.GenYearTimeSt(self.time_ax, year, '판매량')
        else:
            g.GenYearTimeSt(self.time_ax, year, '수량')
        
    def GenDateTimeGraph(self, year, month, date):
        self._mw.stackedWidget_2.setCurrentIndex(4)
        self.time_ax.clear()
        g = GenGraph()
        if(self._mw.coin_time.isChecked()):
            g.GenDateTimeSt(self.time_ax, year, month, date, '판매량')
        else:
            g.GenDateTimeSt(self.time_ax, year, month, date, '수량')
        
    def ProductcalendarPageChanged(self):
        self.productyear = int(self._mw.product_cal.yearShown())
        self.productmonth = int(self._mw.product_cal.monthShown())
        if(self._mw.product_year_check.isChecked()):
            self._mw.product_info_label.setText(str(self.productyear))
            self.GenYearProductGraph(self.productyear)
        else:
            self._mw.product_info_label.setText(str(self.productmonth))
            self.GenMonthProductGraph(self.productyear, self.productmonth)

        
    def SellercalendarPageChanged(self):
        self.selleryear = int(self._mw.seller_cal.yearShown())
        self.sellermonth = int(self._mw.seller_cal.monthShown())
        if(self._mw.seller_year_check.isChecked()):
            self._mw.seller_info_label.setText(str(self.selleryear))
            self.GenYearUserGraph(self.selleryear)
        else:
            self._mw.seller_info_label.setText(str(self.sellermonth))
            self.GenMonthUserGraph(self.selleryear, self.sellermonth)



    def TimecalendarPageChanged(self):
        self.timeyear = int(self._mw.time_cal.yearShown())
        self.timemonth = int(self._mw.time_cal.monthShown())
        if(self._mw.time_year_check.isChecked()):
            self._mw.time_info_label.setText(str(self.timeyear))
            self.GenYearTimeGraph(self.timeyear)
        else:
            self._mw.time_info_label.setText(str(self.timemonth))
            self.GenMonthTimeGraph(self.timeyear, self.timemonth)



    def SellercalendarSelectionChanged(self):
        self.seller_date = self._mw.seller_cal.selectedDate()
        self._mw.seller_info_label.setText(str(self.seller_date.toString()))
        datelist = self.seller_date.toString().split(" ")
        month = int(datelist[1])
        date = int(datelist[2])
        year = int(datelist[3])
        self.GenDateUserGraph(year, month, date)

    def TimecalendarSelectionChanged(self):
        self.time_date = self._mw.time_cal.selectedDate()
        self._mw.time_info_label.setText(str(self.time_date.toString()))
        datelist = self.time_date.toString().split(" ")
        month = int(datelist[1])
        date = int(datelist[2])
        year = int(datelist[3])
        self.GenDateTimeGraph(year, month, date)
    
    def ProductcalendarSelectionChanged(self):
        self.product_date = self._mw.product_cal.selectedDate()
        self._mw.product_info_label.setText(str(self.product_date.toString()))
        datelist = self.product_date.toString().split(" ")
        month = int(datelist[1])
        date = int(datelist[2])
        year = int(datelist[3])
        self.GenDateProductGraph(year, month, date)






# =============================================================================
#       재고 관리 관련
# =============================================================================



    def GetOrigData(self):       
        self.OrigData = self._mw.BusinessTable.currentItem().text() # 원래 수량
                            
       
    def ChangedSomeData(self):

        # 이 내용을 menu manger 시켜도 됨
        Changed_row = self._mw.BusinessTable.currentRow()
        Changed_column = self._mw.BusinessTable.currentColumn()
        Changed_data  = self._mw.BusinessTable.item(Changed_row, Changed_column).text()
        MenuCode = int(self._mw.BusinessTable.item(Changed_row, 0).text())                      # 변경 된 메뉴의 코드를 통해서 값 변경
        

        if Changed_column != 4 :                                                                # 재고 데이터의 수정이 아닌 경우
            self.Errormsg.setText("잘못된 접근입니다!")
            self.Errormsg.exec_()
            self._mw.BusinessTable.cellChanged.disconnect()                                     # 잠깐 감지를 껐다가..
            self._mw.RestoreData(Changed_row,Changed_column,self.OrigData)
            self._mw.BusinessTable.cellChanged.connect(self.ChangedSomeData)                    # 다시 킨다.   
            return
        
        
        for Menu in self._menuManager.MenuList:
            if Menu.code == MenuCode :                
                if(self.if_integer(Changed_data)):                                             # 수정 한 재고 데이터가 숫자가 맞는 경우.
                    Menu.stuck = int(Changed_data)
                    break
                else:
                    self._mw.BusinessTable.cellChanged.disconnect()                            # 잠깐 감지를 껐다가..
                    self._mw.RestoreData(Changed_row,Changed_column,self.OrigData)             # 잘못된 입력에 대해서 다시 되돌림.
                    self._mw.BusinessTable.cellChanged.connect(self.ChangedSomeData)           # 다시 킨다.
                    break
            

        
    def if_integer(self,string):
        try:
            int(string)
            return True
        
        except ValueError:
            self.Errormsg.setText("숫자만 입력 가능합니다!")
            self.Errormsg.exec_()   
            return False
        
        
        
        
    def newMenuRegist(self):
        newMenuInfo = self._mw.getnewMenu()                              # 새로운 메뉴에 대한 데이터 리스트 get
        newCategory = newMenuInfo[1]
        self._menuManager.AddMenu(newMenuInfo)
        self._mw.BusinessTable.cellChanged.disconnect()                  # 잠깐 감지를 껐다가..
        self._mw.MenuUpdate(self._menuManager.MenuList)                  # 업데이트 이후
        self._mw.BusinessTable.cellChanged.connect(self.ChangedSomeData) # 다시 킨다.
       
        for Tb in self._TableList:
            Tb.AppendNewMenu(newCategory)
        
        
        
    