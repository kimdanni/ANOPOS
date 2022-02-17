# -*- coding: utf-8 -*-
"""
Created on Sun Nov 14 16:45:08 2021

@author: kuromi
"""
class Account:
    def __init__(self, _id="", _password="", _permission=False):

        self.__account_id = _id
        self.__account_password = _password
        self.__account_permission = _permission

    @property
    def id(self):
        return self.__account_id

    @id.setter
    def id(self, _id):
        self.__account_id = _id

    @property
    def password(self):
        return self.__account_password

    @password.setter
    def password(self, _password):
        self.__account_password = _password

    @property
    def permission(self):
        return self.__account_permission

    @permission.setter
    def permission(self, _permission):
        self.__account_permission = _permission