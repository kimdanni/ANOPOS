# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:47:44 2021

@author: kuromi
"""

from model.AccountFileManager import AccountFileManager

class AccountManager:
    def __init__(self):
        self.AccountList = [] #각 매니저 객체마다 존재하게 됨
        self.file_manager = AccountFileManager()
        self.file_manager.load(self.AccountList)
        self._id = ""
        self._password = ""
        print("현재 등록 아이디 ", self.AccountList[0].id) 
    def login(self, _id, _password):   
        self._id = _id
        self._password = _password
        for AC in self.AccountList:   
            if(AC.id == _id) :
                #print(AC.id, _id, "Test")                 #해당 아이디가 존재하는가
                if(AC.password == _password):             #비밀번호가 일치하는가
                    print(AC.id,'유저이다. success')
                    return True
                else :
                    print('비밀번호 오류')
                    return False
            
        print('로그인 실패')
        return False        

    def AddAccount(self,_id,_password,_permission):        #root 권한 _permissoion       
        print("회원가입 완료 전 : ", self.AccountList[0].id)   
        self.file_manager.save(_id, _password, _permission)                 
        print(_id,'회원가입 완료')
        print("회원가입 완료 후 : ", self.AccountList[0].id)   

    def IsSameID(self, _id):
        for AC in self.AccountList: 
             if(AC.id == _id) : 
                 print('중복된 아이디')
                 return False
        return True
        