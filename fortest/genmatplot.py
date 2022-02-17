#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 27 23:12:44 2021

@author: mymelo
"""

import pandas as pd
import platform

all_data = pd.read_csv("../sales_data.csv")
all_data.head()

salesdata = pd.DataFrame()

all_data['Month'] = [int(i.split("-")[1]) for i in all_data['날짜']]

all_data.head()

all_data = all_data.dropna(how = "all")

all_data['수량'] = pd.to_numeric(all_data['수량'])
all_data['상품금액'] = pd.to_numeric(all_data['상품금액'])

all_data['판매량'] = all_data['수량'] * all_data['상품금액']

all_data.head()

all_data.groupby('Month').sum()

import matplotlib.pyplot as plt

months = range(1, 13)
results = all_data.groupby('Month').sum()
plt.bar(months, results['판매량'])
plt.show()

months = range(1, 13)
results = all_data.groupby('Month').sum()
plt.bar(months, results['수량'])
plt.show()

result2 = all_data.groupby('판매자').sum()
result2

saleman = all_data['판매자'].unique()

plt.bar(saleman, result2['판매량'])
plt.xticks(saleman, rotation='vertical', size = 8)
labels, location = plt.yticks()
plt.yticks(labels, (labels/1000).astype(int))
plt.ylabel('sales (sales / 1000)')
plt.xlabel('user')
plt.show()

saleman = all_data['판매자'].unique()

plt.bar(saleman, result2['수량'])
plt.xticks(saleman, rotation='vertical', size = 8)
labels, location = plt.yticks()
plt.yticks(labels, (labels/1000).astype(int))
plt.ylabel('sales (sales / 1000)')
plt.xlabel('user')
plt.show()

import numpy as np

# 언제 광고를 표시하는게 적합할까

all_data.head()
all_data['시간'] = pd.to_datetime(all_data['시간'])
all_data.head()

all_data['hour'] = all_data['시간'].dt.hour
all_data.head()

result3 = all_data.groupby(["hour"]).sum()

result3

result3 = all_data.groupby(['hour'])
saleman = all_data['판매자'].unique()

plt.bar(saleman, result2['수량'])
plt.xticks(saleman, rotation='vertical', size = 8)
labels, location = plt.yticks()
plt.yticks(labels, (labels/1000).astype(int))
plt.ylabel('sales (sales / 1000)')
plt.xlabel('user')
plt.show()

import numpy as np
from scipy.signal import savgol_filter

all_data.head()

result3 = all_data.groupby(['hour'])['수량'].sum()
hours = [hour for hour, df in all_data.groupby('hour')]
plt.plot(hours, result3)
plt.xticks(hours)
plt.grid()
plt.show()

result3 = all_data.groupby(['hour'])['판매량'].count()
hours = [hour for hour, df in all_data.groupby('hour')]

plt.plot(hours, result3)
plt.xticks(hours)
plt.grid()
plt.show()

all_data.head()

new_all = all_data[all_data['상품명'].duplicated(keep=False)]
new_all.head()


import matplotlib.pyplot as plt
if platform.system() == 'Darwin': #맥
    plt.rc('font', family='AppleGothic') 
elif platform.system() == 'Windows': #윈도우
    plt.rc('font', family='Malgun Gothic') 
elif platform.system() == 'Linux':
    plt.rc('font', family='Malgun Gothic') 
product_group = all_data.groupby('상품명')

quantity_ordered = product_group.sum()['수량']

products = [product for product, df in product_group]

plt.bar(products, quantity_ordered)
plt.ylabel('수량')
plt.xlabel('상품명')
plt.xticks(products, rotation='vertical', size = 11)
plt.show()

prices = all_data.groupby('상품명').mean()['상품금액']

fig, ax1 = plt.subplots()

ax2 = ax1.twinx()
ax1.bar(products, quantity_ordered, color = 'orange')
ax2.plot(products, prices, 'b-')

ax1.set_xlabel('상품명')
ax1.set_ylabel('상품 금액', color='black')
ax2.set_ylabel('price', color='black')
ax1.set_xticklabels(products, rotation='vertical', size = 8)
plt.show()