# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:45:58 2021

@author: kuromi
"""

from model.Account import Account
import pickle

class AccountFileManager:

    def load(self,AccountList):
         f = None      
         try :
             f = open('account.pkl', 'rb')
             while True :     
                 try :
                     tempAccount = pickle.load(f) 
                 except EOFError:
                     break                                     
                 AccountList.append(tempAccount)
    
         except IOError:
             account = Account('admin', '1234', True)          #root 권한 True
             AccountList.append(account)
             pickle.dump(account,open('account.pkl','wb')) 
             print('파일 존재하지않음 - admin 계정 생성')
       
         finally :
             if f :
                 f.close()

    def save(self,_id, _password, _permission):
        pickle.dump(Account(_id, _password, _permission),open('account.pkl','ab'))  
