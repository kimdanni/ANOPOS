# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 16:44:46 2021

@author: JY-PC
"""
import copy
class Table:                             # 각 테이블마다 존재, 0~7 : 매장 식사 8 : TakeOut
    _MenuList = []                       # 클래스 변수(공동 사용) - 전체 메뉴의 데이터(가격, 수량, 이름, 번호 등)가 저장된 리스트
    def __init__(self, MenuList, TableNumber):
        Table._MenuList = MenuList
        
        self._TableNumber = TableNumber
        
        self._orderList = []                  # 주문한 리스트 저장
        self._CardPay = False
        self._CashPay = False
        self._Receipt_A = False
        self._Receipt_B = False
        
        self._setClear = True
        
        self._setDate = ''
        
        self._TotalPrice = 0
        self._TableMenuListOrig = self.GetMenuList(TableNumber)
        print("init origin total num",self._TableMenuListOrig[0].stuck)
        self._TableMenuList = copy.deepcopy(self._TableMenuListOrig) # 주문 가능한 메뉴 리스트
        print("init cp total num",self._TableMenuList[0].stuck)
    
    def GetMenuList(self,TableNumber):  # 전체 메뉴리스트에서 매장내 식사 or 테이크 아웃에 따른 표시할 메뉴 항목 반환
        TableMenuList = []    
        if TableNumber == 8 :
            for Menu in Table._MenuList:
                   if Menu.category == "테이블" :         
                       TableMenuList.append(Menu)             

                       
        else :
            for Menu in Table._MenuList :
                if Menu.category != "테이블" and Menu.category != "부재료" :
                       TableMenuList.append(Menu)

        return TableMenuList
    
    def AppendNewMenu(self,Category):  # 신 메뉴 추가
        if self._TableNumber == 8 and Category == "테이블" :       
              self._TableMenuListOrig.append(Table._MenuList[-1])

        elif Category != "테이블" :
             self._TableMenuListOrig.append(Table._MenuList[-1])
  

  
    
    #주문 추가
    def AppendOrder(self, Menuindex, amount):                    # TalbelMenuList에 저장된 메뉴들의 순서와 Table Widget의 index순서는 당연히 같음.
        _menuName = self._TableMenuListOrig[Menuindex].menuName      # 메뉴 명
        _amount = int(amount)                                         # 주문 수량
        _price = int(self._TableMenuListOrig[Menuindex].price)            # 가격 
        self._TotalPrice += (_price * _amount) # 가격 총합
        templist = [ _menuName, _amount, _price] 
        
        self._orderList.append(templist)
        
        for Menu in Table._MenuList :
            if _menuName == Menu.menuName:
                Menu.stuck -= _amount
        self._setClear = False
     

    # 주문 취소
    def Reset(self):
        for orderMenu in self._orderList: # 삭제할 메뉴 수만큼(주문한 메뉴 수)반복
            for Menu in Table._MenuList:
                if Menu.menuName == orderMenu[0] : # 메뉴 이름과 동일한 메뉴를 찾아서        
                    Menu.stuck += orderMenu[1]     # 주문했던 수량만큼을 다시 더해준다.               
                    break
                            
        self._orderList.clear() # 주문 넣어 뒀던 리스트 초기화
        self._TotalPrice = 0    # 가격도 초기화
        
        
    
    @property
    def TableMenuList(self):
        return self._TableMenuListOrig
        
    @property
    def TableOrderList(self):
        return self._orderList
        
    @property
    def TotalPrice(self):
        return self._TotalPrice
    
    @TotalPrice.setter
    def TotalPrice(self, Totalprice):
        self._TotalPrice = Totalprice
        
    def orderlistclear(self):
        self._orderList.clear()









