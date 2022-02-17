class Menu:
                          #  코드   카테고리    메뉴명    가격   부자재[리스트]   수량
    def __init__(self, __code, __category, __menuName, __price, __sublist, __stuck):

        self._code = __code
        self._category = __category
        self._menuName = __menuName
        self._price = __price
        self._sublist = __sublist
        self._stuck = __stuck

    @property
    def code(self):
        return self._code

    @code.setter
    def code(self, __code):
        self._code = __code
    
    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, __category):
        self._category = __category
    

    @property
    def menuName(self):
        return self._menuName

    @menuName.setter
    def menuName(self, __menuName):
        self._menuName = __menuName  

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, __price):
        self._price = __price

    @property
    def sublist(self):
        return self._sublist

    @sublist.setter
    def sublist(self, __sublist):
        self._sublist = __sublist

    @property
    def stuck(self):
        return self._stuck

    @stuck.setter
    def stuck(self, __stuck):
        self._stuck = __stuck
    
  