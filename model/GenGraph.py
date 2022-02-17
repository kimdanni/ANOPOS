#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 23:04:27 2021

@author: mymelo
"""
import pandas as pd
import platform
import numpy as np
import matplotlib.pyplot as plt

class GenGraph:
    def __init__(self):
        self.all_data = pd.read_csv("salesdata.csv")
        
        print(self.all_data['날짜'].head())
        self.all_data['Year'] = [int(i.split("-")[0]) for i in self.all_data['날짜']]
        self.all_data['Month'] = [int(i.split("-")[1]) for i in self.all_data['날짜']]
        self.all_data['Date'] = [int(i.split("-")[2]) for i in self.all_data['날짜']]
        
        self.all_data = self.all_data.dropna(how = "all")
        
        self.all_data['수량'] = pd.to_numeric(self.all_data['수량'])
        self.all_data['상품금액'] = pd.to_numeric(self.all_data['상품금액'])
        
        self.all_data['판매량'] = self.all_data['수량'] * self.all_data['상품금액']
        
        self.all_data.groupby('Month').sum()
        self.all_data['시간'] = pd.to_datetime(self.all_data['시간'])
        self.all_data['hour'] = self.all_data['시간'].dt.hour
    
    def TotalSales(self):
        data = []
        data.append(self.all_data['판매량'].sum())
        data.append(self.all_data['수량'].sum())
        data.append(self.all_data['판매자'].max())
        return data
    
    def GenMonthSt(self, label):
        result3 = self.all_data.groupby(['Month'])['판매량'].count()
        hours = [hour for hour, df in self.all_data.groupby('Month')]
        label.plot(hours, result3)
        label.figure.canvas.draw()
    
    
    ## product 관련
    def GenProductSt(self, label, option):
        product_group = self.all_data.groupby('상품명')

        quantity_ordered = product_group.sum()[option]

        products = [product for product, df in product_group]

        label.bar(products, quantity_ordered)
        for l in label.xaxis.get_ticklabels() :
            l.set_rotation(45)
        label.figure.canvas.draw()
        
    def GenYearProductSt(self, label, year, option):
        mask1 = (self.all_data['Year'] == year)
        all_data = self.all_data.loc[mask1, :]
        product_group = all_data.groupby('상품명')

        quantity_ordered = product_group.sum()[option]

        products = [product for product, df in product_group]

        label.bar(products, quantity_ordered)
        for l in label.xaxis.get_ticklabels() :
            l.set_rotation(45)
        label.figure.canvas.draw()
        
    def GenMonthProductSt(self, label, year, month, option):
        mask = (self.all_data['Month'] == month)
        mask1 = (self.all_data['Year'] == year)
        all_data = self.all_data.loc[mask1 & mask, :]
        
        product_group = all_data.groupby('상품명')

        quantity_ordered = product_group.sum()[option]

        products = [product for product, df in product_group]

        label.bar(products, quantity_ordered)
        for l in label.xaxis.get_ticklabels() :
            l.set_rotation(45)
        label.figure.canvas.draw()
        
    def GenDateProductSt(self, label, year, month, date, option):
        mask = (self.all_data['Month'] == month)
        mask1 = (self.all_data['Year'] == year)
        mask2 = (self.all_data['Date'] == date)
        all_data = self.all_data.loc[mask1 & mask & mask2, :]
        
        product_group = all_data.groupby('상품명')

        quantity_ordered = product_group.sum()[option]

        products = [product for product, df in product_group]

        label.bar(products, quantity_ordered)
        for l in label.xaxis.get_ticklabels() :
            l.set_rotation(45)
        label.figure.canvas.draw()
    
    
    
    ## user 관련
    def GenUserSt(self, label , option):
        saleman = self.all_data['판매자'].unique()
        result2 = self.all_data.groupby('판매자').sum()
        label.bar(saleman, result2[option])
        label.figure.canvas.draw()
        
    def GenDateUserSt(self, label, year, month, date, option):
        mask = (self.all_data['Month'] == month)
        mask1 = (self.all_data['Year'] == year)
        mask2 = (self.all_data['Date'] == date)
        
        all_data = self.all_data.loc[mask1 & mask & mask2, :]
        saleman = all_data['판매자'].unique()
        result2 = all_data.groupby('판매자').sum()
        label.bar(saleman, result2[option])
        label.figure.canvas.draw()
        
    def GenMonthUserSt(self, label, year, month, option):
        mask = (self.all_data['Month'] == month)
        mask1 = (self.all_data['Year'] == year)
        all_data = self.all_data.loc[mask1 & mask, :]
        print(all_data.head())
        saleman = all_data['판매자'].unique()
        result2 = all_data.groupby('판매자').sum()
        label.bar(saleman, result2[option])
        label.figure.canvas.draw()
    
    def GenYearUserSt(self, label, year, option):
        mask = (self.all_data['Year'] == year)
        all_data = self.all_data.loc[mask, :]
        saleman = all_data['판매자'].unique()
        result2 = all_data.groupby('판매자').sum()
        label.bar(saleman, result2[option])
        label.figure.canvas.draw()
    
    
    ## TIME 관련
    def GenTimeSt(self, label, option):
        result3 = self.all_data.groupby(['hour'])[option].count()
        hours = [hour for hour, df in self.all_data.groupby('hour')]
        label.plot(hours, result3)
        label.figure.canvas.draw()
        
    def GenDateTimeSt(self, label, year, month, date, option):
        mask = (self.all_data['Month'] == month)
        mask1 = (self.all_data['Year'] == year)
        mask2 = (self.all_data['Date'] == date)
        
        all_data = self.all_data.loc[mask1 & mask & mask2, :]
        result3 = all_data.groupby(['hour'])[option].count()
        hours = [hour for hour, df in all_data.groupby('hour')]
        label.plot(hours, result3)
        label.figure.canvas.draw()
        
    def GenMonthTimeSt(self, label, year, month, option):
        mask = (self.all_data['Month'] == month)
        mask1 = (self.all_data['Year'] == year)
        all_data = self.all_data.loc[mask1 & mask, :]
        result3 = all_data.groupby(['hour'])[option].count()
        hours = [hour for hour, df in all_data.groupby('hour')]
        label.plot(hours, result3)
        label.figure.canvas.draw()
    
    def GenYearTimeSt(self, label, year, option):
        mask = (self.all_data['Year'] == year)
        all_data = self.all_data.loc[mask, :]
        result3 = all_data.groupby(['hour'])[option].count()
        hours = [hour for hour, df in all_data.groupby('hour')]
        label.plot(hours, result3)
        label.figure.canvas.draw()
        
        
if __name__ == '__main__':
    g = GenGraph()
    g.TotalSales()