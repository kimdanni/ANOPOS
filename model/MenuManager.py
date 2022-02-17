# -*- coding: utf-8 -*-
"""
Created on Tue Nov 16 01:29:43 2021

@author: JY-PC
"""
from model.MenuCSVManager import MenuCSVManager


class MenuManager:

    def __init__(self):
        self.menuList = []         #메뉴 객체들이 저장된 리스트
        self.csv_manager = MenuCSVManager()
        self.csv_manager.loadCSV(self.MenuList)
    
    @property
    def MenuList(self):
        return self.menuList
    
    # 메뉴 추가 
    #상품 정보 리스트 구조(ex) : [코드, 카테고리, 메뉴명, 가격, 부자재(리스트), 수량 ]    
    def AddMenu(self, NewList): 
        for Menu in self.menuList:
            if Menu.code == NewList[0] :
                print('코드가 중복됨.')
                return
            if Menu.menuName == NewList[2] :
                print('항목(이름)이 중복됨.')
                return
        
        self.csv_manager.AddNewMenu(self.menuList, NewList) # 새로운 메뉴 리스트 추가                 

    def AddStuck(self, _code, _stuck): # 재고 추가
        for Menu in self.menuList:
            if Menu.code == _code :
                Menu.stuck = _stuck
                return

        print('해당 메뉴코드가 존재하지 않음.')
        

    def SaveCSV(self): # CSV 파일저장.
        self.csv_manager.saveCSV(self.MenuList) # 현재 메뉴 리스트를 csv파일에 저장 







# =============================================================================
      #TEST FUCNTION
if __name__ == '__main__':
    a = MenuManager()
    a.AddStuck(4, 100)
   # a.MenuList(1)
    #print(a.MenuList(1)[0])
    a.SaveCSV()
# =============================================================================








