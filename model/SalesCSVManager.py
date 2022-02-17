# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 01:55:45 2021

@author: kuromi
"""
import pandas as pd
import csv

class SalesCSVManager:
    def __init__(self):
        self.__cpdir = 'salesdata_modify.csv'
        self.__dir = 'salesdata.csv'
        #shutil.copy2(self.__dir,self.__cpdir)
# =============================================================================
#     def loadCSV(self,MenuList):
#          data = pd.read_csv(self.__dir,encoding='cp949')
#          for i in range(len(data)):
#              dlist = list(data.iloc[i]) #전체 데이터
#                         #  재료1      재료2     재료3
#              sublist = [dlist[4], dlist[5], dlist[6]]
#                              #  코드   카테고리    메뉴명    가격      부재료      수량
#              tempMenu = Menu(dlist[0], dlist[1], dlist[2], dlist[3], sublist, dlist[7])    
#         
#              MenuList.append(tempMenu)
# =============================================================================
      
    def saveCSV(self,MenuList, user): #일단은 덮어쓰기 안 되도록 해놨습니다.       
        with open(self.__dir, 'a+', encoding='utf-8-sig', newline='') as csvfile: 
            #Info_List = ['상품명','수량','상품금액', '날짜', '시간','판매자'] 
            writer = csv.writer(csvfile)
            # if(f.read().count("\n") == 0):
            #     writer.writerow(Info_List)
            for Menu_ in MenuList:
                Menu_.append(user)
                writer.writerow(Menu_)


# =============================================================================
#     def AddNewMenu(self, MenuList, NewList): #새로운 리스트(메뉴)객체 생성 및 추가
#         tempMenu = Menu(NewList[0], NewList[1], NewList[2], NewList[3], NewList[4], NewList[5])
#         MenuList.append(tempMenu)
# =============================================================================
