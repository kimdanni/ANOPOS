# -*- coding: utf-8 -*-
"""
Created on Thu Nov 25 02:38:38 2021

@author: kuromi
"""
import pandas as pd
import csv
import shutil
import random

class createData:
    def __init__(self,):
        self.__mdays = [31,28,31,30,31,30,31,31,30,31,30,31]

        self.__cpdir = 'sample_data.csv'
        self.__dir = 'sample_data.csv'
        self.__year = ["2021", "2020", "2022", "2023", "2024", "2025"]
        self.__user = ["admin", "kuromi", "mymelo", "anohana", "legend"]
        self.__menu = ["plant","gollem","water","mushrom","history","sord","jelly","dinner","party table","courage","gollem's sweat","fairly","gold"]
        # 골렘의 땀을 여름철 특선 메뉴로 index 8
        # 마법 버섯을 겨울철 특선 메뉴로 index 3
        # 요정 가루를 특정 날의 특선 메뉴로 index 9
        self.__cost = [str(i) for i in [300,3000,480,3200,5000,4000,400,500,1000,3000,1500]]
    def genDate(self, option = ["", ""]):
        Info = []
        
        
        month = list(range(1, 13))
        currentmonth = 0
        
        
        monthweight = [1] * 12
        monthweight[11] = 4
        monthweight[0] = 6

        coldMonth = [11, 12, 1]
        hotMonth = [5,6,7]
        specialdate = [7, 11]
        
        date = ""
        datewieght = [1] * self.__mdays[currentmonth-1]
        currentdate = 0
        
        
        if(option[0] == "Y"):
            date += str(random.choices(self.__year, weights = (1, 6, 3, 2, 5, 10), k = 1)[0])
        else:
            date += str(random.choices(self.__year)[0])
            
            
        if(option[1] == "Y"):
            currentmonth = random.choices(month , weights = monthweight, k = 1)[0]
            if currentmonth in coldMonth:
                Info.append("cold")
            if currentmonth in hotMonth:
                Info.append("hot")
        else:
            currentmonth = random.choice(month)
        
        date += "-"
        date += str(currentmonth)
        date += "-"
        
            
        if(option[2] == "Y"):
            dateList = list(range(1, self.__mdays[currentmonth-1] + 1))
            dateWeight = [1] * self.__mdays[currentmonth-1]
            dateWeight[11] = 8
            dateWeight[1] = 5
            currentdate = random.choices(dateList, weights = dateWeight, k = 1)[0]
            
            if currentdate in specialdate:
                Info.append("specialdate")
        else:
            currentdate = list(range(1, self.__mdays[currentmonth-1] + 1))
        
        date += str(currentdate)
        
        if(len(Info) == 0):
            Info.append("")
            Info.append("")
        if(len(Info) == 1):
            Info.append("")
        return date, Info
        
    
    def turnType(self, num):
        if(int(num / 10) == 0):
            tmp = "0"
            tmp += str(num)
            num = tmp
            return tmp
        return str(num)
    
    def genTime(self, option = ""):
        time = ""
        currenthour = 0
        hour = random.randint(0, 23)
        hourList = list(range(0, 24))
        hourWeight = [1] * 24
        if(option == "hour"):
            for i in range(8, 14):
                hourWeight[i] = hourWeight[i] * 1.5
                if(i == 13):
                    hourWeight[i] = 15
            
            for i in range(14, 19):
                hourWeight[i] = hourWeight[i] * 1.6
                if(i == 17):
                    hourWeight[i] = 18
                hourWeight[i] = hourWeight[i - 1] / 1.6
                    
            currenthour = str(random.choices(hourList, weights = hourWeight, k = 1)[0])
        else:
            currenthour = random.choices(hourList)
            
        minute = random.randint(0, 59)
        
        hour = self.turnType(hour)
        time += hour
        time += ":"
        
        minute = self.turnType(minute)
        
        time += minute
        
        return time
    
    def saveCSV(self, dataSize): #일단은 덮어쓰기 안 되도록 해놨습니다.       
        with open(self.__dir, 'a+', encoding='utf-8-sig', newline='') as f: 
            Info_List = ['상품명','수량','상품금액', '날짜', '시간','판매자']    
            writer = csv.writer(f)
            menuweight = [1] * 11
            index = 0
            if (f.read().count("\n") == 0):
                writer.writerow(Info_List)
            for i in range(dataSize):
                date, option = self.genDate(['Y','Y','Y'])
                time = self.genTime('hour')
                menuIndex = list(range(0, 11))
                if(option[0] == "cold"):
                    menuweight[3] = 9
                    menuweight[8] = 0
                    index = random.choices(menuIndex, weights = menuweight, k = 11)[0]
                    if(index == 8):
                        dataSize += 1
                        continue
                elif(option[0] == "hot"):
                    menuweight[8] = 9
                    menuweight[3] = 0
                    index = random.choices(menuIndex, weights = menuweight, k = 11)[0]
                    if(index == 3):
                        dataSize += 1
                        continue
                elif(option[1] == "specialdate"):
                    menuweight[9] = 9
                    index = random.choices(menuIndex, weights = menuweight, k = 11)[0]
                    if(dataSize % i == 0):
                        index = 9
                else:
                    if(index == 8 or index == 3):
                        dataSize += 1
                        continue
                    index = random.choices(menuIndex, weights = menuweight, k = 11)[0]
                tmpList = []
            
                tmpList.append(self.__menu[index])
                tmpList.append(str(random.randint(1,10)))
                tmpList.append(self.__cost[index])
                tmpList.append(date)
                tmpList.append(time)
                tmpList.append(random.choices(self.__user, weights = (3, 5, 7, 10, 20), k = 1)[0]) # legend 유저는 물건을 잘팜
                tmpList.append(None)
                writer.writerow(tmpList)


if __name__ == '__main__':
    c = createData()
    c.saveCSV(100000)