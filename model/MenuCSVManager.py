# -*- coding: utf-8 -*-
"""
Created on Mon Nov 15 23:38:43 2021

@author: JY-PC
"""
import pandas as pd
import csv
from model.Menu import Menu
import shutil

class MenuCSVManager:
    def __init__(self):
        self.__cpdir = 'menudata_modify.csv'
        self.__dir = 'menudata.csv'
        #shutil.copy2(self.__dir,self.__cpdir)
    def loadCSV(self,MenuList):
         data = pd.read_csv(self.__dir,encoding='cp949')
         for i in range(len(data)):
             dlist = list(data.iloc[i]) #전체 데이터
                        #  재료1      재료2     재료3
             sublist = [dlist[4], dlist[5], dlist[6]]
                             #  코드   카테고리    메뉴명    가격      부재료      수량
             tempMenu = Menu(dlist[0], dlist[1], dlist[2], dlist[3], sublist, dlist[7])    
        
             MenuList.append(tempMenu)
      
    def saveCSV(self,MenuList): #일단은 덮어쓰기 안 되도록 해놨습니다.       
        with open(self.__dir, 'w', newline='') as f: 
            Info_List = ['상품코드','카테고리','품명', '판매가', '하위1','하위2','하위3','재고']    
            writer = csv.writer(f)
            writer.writerow(Info_List)
            for Menu_ in MenuList:
                tempList = [Menu_.code, Menu_.category, Menu_.menuName, Menu_.price, 
                           Menu_.sublist[0], Menu_.sublist[1], Menu_.sublist[2], Menu_.stuck] 

                writer.writerow(tempList)


    def AddNewMenu(self, MenuList, NewList): #새로운 리스트(메뉴)객체 생성 및 추가
        tempMenu = Menu(NewList[0], NewList[1], NewList[2], NewList[3], NewList[4], NewList[5])
        MenuList.append(tempMenu)