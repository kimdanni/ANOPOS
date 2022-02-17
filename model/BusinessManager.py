# -*- coding: utf-8 -*-
"""
Created on Sat Nov 20 16:44:46 2021

@author: JY-PC
"""
import copy
class BusinessManager:                            
    _MenuList = []                     
    def __init__(self):
        Table._MenuList = MenuList
        
        self._TableNumber = TableNumber
        
        self._orderList = []                  # 주문한 리스트 저장
        self._CardPay = False
        self._CashPay = False
        self._Receipt_A = False
        self._Receipt_B = False
        
        self._setClear = True
        
        self._setDate = ''
        
    def GetMenuList(self,MenuList):  # 전체 메뉴리스트에서 매장내 식사 or 테이크 아웃에 따른 표시할 메뉴 항목 반환
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
    
    
    #주문 추가
    def AppendOrder(self, Menuindex, amount):                    # TalbelMenuList에 저장된 메뉴들의 순서와 Table Widget의 index순서는 당연히 같음.
        _menuName = self._TableMenuList[Menuindex].menuName      # 메뉴 명
        _amount = int(amount)                                         # 주문 수량
        _price = int(self._TableMenuList[Menuindex].price)            # 가격 
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
        










