import os

class LightController():
    def __init__(self,myApp,lightStateListener):
        self.lightIsOpen = False
        self.lightStateCallBack = lightStateListener

        self.__controlValueUrl = 'Light/LightState'

        self.__myApp = myApp
        self.__wilddogMgr = self.__myApp.GetWilddogMgr()
        self.__wilddogMgr.AddWilddogCallback(self.WilddogCallBack)

        #self.ble = BleDevice()

        #print(self.ble.scane())
        #self.bleDevice = self.ble.connect_name("Light2.1")  # 修改成设备名字

        #self.chars = self.ble.discover_characteristics(self.bleDevice)
        #print(self.chars) # uuid
        #self.InitLight()
    def WilddogCallBack(self,wilddogInfo):
        lightStatus = int(wilddogInfo["Light"]["LightState"])
        print(lightStatus)
        if(lightStatus==1):
            self.ChargeLightControllerState()
        else:
            self.ChargeLightControllerState()

    def ChargeLightControllerState(self):
        if(self.lightIsOpen):
            self.__wilddogMgr.UpdateWilddogNodeValue(self.__controlValueUrl,"0")
            os.system("sudo hciconfig hci0 up")
            os.system("sudo gatttool -i hci0 -b 00:02:5B:00:83:41 --char-write-req -a 0x0022 -n 0x0001")
        else:
            self.__wilddogMgr.UpdateWilddogNodeValue(self.__controlValueUrl, "1")
            os.system("sudo hciconfig hci0 up")
            os.system("sudo gatttool -i hci0 -b 00:02:5B:00:83:41 --char-write-req -a 0x0022 -n 0x0000")
    def InitLight(self):
        #print(self.ble.read_characteristics(self.chars[1]['uuid'])) #根据值设置lightIsOpen 属性
        self.lightIsOpen = False
        if (self.lightStateCallBack != None):
            self.lightStateCallBack(self.lightIsOpen)

    def OpenLight(self):
        self.lightIsOpen = True
        #self.ble.write_characteristics("0x0001", self.chars[0]['uuid'])
        #self.ble.write_characteristics("0x0001", "0x0022")
        if(self.lightStateCallBack!=None):
            self.lightStateCallBack(self.lightIsOpen)
    def CloseLight(self):
        self.lightIsOpen = False
        #self.ble.write_characteristics("hello world", self.chars[0]['uuid'])
        #self.ble.write_characteristics("0x0001", "0x0022")
        if (self.lightStateCallBack != None):
            self.lightStateCallBack(self.lightIsOpen)


