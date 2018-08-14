# -*- coding: utf-8 -*-
from PyQt4.QtCore import QTimer
from PyQt4 import QtGui
from wilddog import wilddog


class MyWilddog(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        #your_storageyour_storage
        self.__wilddog = wilddog.WilddogApplication('https://wd6711391518tgqjft.wilddogio.com', None)
        result = self.__wilddog.get('/Flagmingo', 'Curtain')

        self.__wilddogCallBack = []

    def AddWilddogCallback(self,func):
        self.__wilddogCallBack.append(func)

    def RemoveWilddogCallback(self,func):
        self.__wilddogCallBack.remove(func)

    def UpdateWilddogNodeValue(self,nodeurl,value):
        self.__wilddog.put_async('/Flagmingo',nodeurl , value)
    def DeleteWilddogNodeValue(self,nodeurl):
        self.__wilddog.delete_async('/Flagmingo',nodeurl)

    def StartReadUrlLoop(self, loopTime):
        self._listenWebTimer = QTimer(self)
        self._listenWebTimer.setInterval(loopTime*1000)
        self._listenWebTimer.timeout.connect(self.__GetUrl)
        self._listenWebTimer.start()

    def StopReadUrlLoop(self):
        if(self._listenWebTimer.isActive()):
            self._listenWebTimer.stop()

    def __GetUrl(self):
        self.__result = self.__wilddog.get('/Flagmingo', None)
        for callbackfunc in self.__wilddogCallBack:
            callbackfunc(self.__result)

        # self._func(self.wilddog.get('/Flagmingo', None))



