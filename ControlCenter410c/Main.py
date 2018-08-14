import sys
import Code.Curtain.CurtainModule
import Code.Light.LightManager
import Code.Common.AppDataManager
import Code.Common.IOManager
import Code.Common.WilddogManager
import _thread

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QTimer
from UI.UIControlCenter import Ui_MainWindow

class MyApp(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self._isTestMode = False  # If Test Mode

        # Base Module Init
        self.__timeMgr = Code.Common.TimeManager.TimeMgr()
        self.__appDataMgr = Code.Common.AppDataManager.DataMsg()
        self.__sysDataTime = self.__timeMgr.GetSystemDataTime()
        self.UpdateDataTimeLabel(self.__sysDataTime)
        self.__timeMgr.StartUpdateDataTime(self.UpdateDataTimeLabel)
        self.__ioMgr = Code.Common.IOManager.IOMgr()

        # Wilddog Init
        self.__wilddogMgr = Code.Common.WilddogManager.MyWilddog()
        self.__wilddogMgr.StartReadUrlLoop(self.__appDataMgr.WilddogLoopTimer)
        self.__wilddogMgr.UpdateWilddogNodeValue('smoke',108)

        # Light Inits
        self.__lightModule = Code.Light.LightManager.LightController(self,self.UpdateLightState)

        # Curtain Init
        self.__curtainModule = Code.Curtain.CurtainModule.MyCurtainModule(self)

        # Tip UI Timer
        self._tipTimer = QTimer(self)
        self._tipTimer.setSingleShot(True)
        self._tipTimer.timeout.connect(lambda: self.TipLabel.setText(""))

        #start a thread
        try:
            _thread.start_new_thread(self.readDataFromFile,'/sys/devices/platform/soc/soc:qca4020/value')
        except:
            print('excute fail!')

    # get and set properties
    def GetSysDataTime(self):
        return self.__sysDataTime
    def GetAppDataMgr(self):
        return  self.__appDataMgr
    def GetTimeMgr(self):
        return  self.__timeMgr
    def GetIOMgr(self):
        return self.__ioMgr
    def GetWilddogMgr(self):
        return self.__wilddogMgr

    #define a function to read
    def readDataFromFile(self,path):
        while True:
            try:
                f = open(path,'r')
                line = f.readline()
                print(line)
                self.__wilddogMgr.UpdateWilddogNodeValue('smoke',line)
                f.close()
            finally:
                if (f):
                  f.close()

    # IO functions
    def GetIOPath(self):
        path = ""
        if (self._isTestMode):
            path = self.__appDataMgr.TestIOFilePath
        else:
            path = self.__appDataMgr.IOFilePath
        return path

    # UI Call Back
    def OnCurtainSliderReleased(self):
        self.__curtainModule.OnSliderReleased()
    def OnCurtainAddMissionClicked(self):
        self.MissionDataTime.setDateTime(self.__sysDataTime)
        self.__curtainModule.OnAddMissionClicked()
    def OnCurtainDeleteMissionClicked(self):
        self.__curtainModule.OnDeleteMissionClicked()
    def OnCurtainMissionComfirmClicked(self):
        self.__curtainModule.OnConfirmBtnClicked()
    def OnCurtainMissionCancelClicked(self):
        self.__curtainModule.OnCancelBtnClicked()
    def OnControlPlaneCurrentChanged(self,index):
        print("OnControlPlaneCurrentChanged"+str(index))
        pass
    def OnLightControlBtnClicked(self):
        print("OnLightControlBtnClicked")
        self.__lightModule.ChargeLightControllerState()

    # UI Public Functions
    def ShowTip(self, TipStr, waitTime=3):
        self.TipLabel.setText(TipStr)
        if (self._tipTimer.isActive()):
            self._tipTimer.stop()
        self._tipTimer.start(waitTime * 1000)

    # CallBack Function
    def UpdateDataTimeLabel(self, dataTime):
        self.__sysDataTime = dataTime
        self.DateLabel.setText(dataTime.toString(self.__appDataMgr.DataFormat))
        self.TimeLabel.setText(dataTime.toString(self.__appDataMgr.TimeFormat))
    def UpdateLightState(self,lightIsOpen):
        print(lightIsOpen)
        if lightIsOpen:
            self.ControlBtnTip.setText(self.__appDataMgr.LocalizationMsg.LightTipTextOpened)
            self.ControlLightBtn.setText(self.__appDataMgr.LocalizationMsg.LightBtnTextOpened)
            pass
        else:
            self.ControlBtnTip.setText(self.__appDataMgr.LocalizationMsg.LightTipTextClosed)
            self.ControlLightBtn.setText(self.__appDataMgr.LocalizationMsg.LightBtnTextClosed)
            pass
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())




