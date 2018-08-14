import Code.Common.TimeManager
import Code.Common.IOManager
import Code.Common.AppDataManager
import Code.Curtain.CurtainManager
import datetime
import  time
from PyQt4 import QtGui
from PyQt4.QtCore import QTimer

class MyCurtainModule(QtGui.QMainWindow):
    def __init__(self, MyApp):
        QtGui.QMainWindow.__init__(self)
        self.myApp = MyApp

        # Value Properties
        self.missionList = []
        self.__controlValueUrl = 'Curtain/ControlValue'
        self.__missionListUrl = 'Curtain/MissionList'
        self.__missionTimeKey = '_MissionTime'
        self.__missionValueKey = '_MissionValue'
        self.__lastMissionList = None

        # Module Properties
        self.__appDataMgr = self.myApp.GetAppDataMgr()
        self.__wilddogMgr = self.myApp.GetWilddogMgr()
        self.__timeMgr = self.myApp.GetTimeMgr()
        self.__wilddogMgr.AddWilddogCallback(self.WilddogCallBack)

        # Curtain Init
        self.__curtain = Code.Curtain.CurtainManager.Curtain(self.myApp, 16)
        self.__curtain.CommandStopCallBack.append(self.OnCurtainStop)
        self.__curtain.CommandStartCallBack.append(self.OnCurtainStart)
        self.__curtain.CommandRunningCallBack.append(self.OnCurtainPosUpdate)
        self.__curtain.CurtainResetingCallBack.append(self.OnCurtainReseting)

       # if(not self.myApp._isTestMode):
           # self._curtain.ResetCurtain() # 重置初始化

        # UI Init

        self.myApp.CurtainControlSlider.setMaximum(self.__curtain.CurtainRunTime)
        self.myApp.ControlCurtainTip.setText(self.__appDataMgr.LocalizationMsg.ControlSliderOperationTipStr)

        self.myApp.AddMissionBtn.setText(self.__appDataMgr.LocalizationMsg.AddMissionBtnStr)
        self.myApp.DeleteMissionBtn.setText(self.__appDataMgr.LocalizationMsg.DeleteMissionBtnStr)
        self.myApp.ComfirmBtn.setText(self.__appDataMgr.LocalizationMsg.ComfirmBtnStr)
        self.myApp.CancelBtn.setText(self.__appDataMgr.LocalizationMsg.CancelBtnStr)

        self.myApp.MissionTitle.setText(self.__appDataMgr.LocalizationMsg.MissionTitleStr)
        self.myApp.MissionSlider.setMaximum(self.__curtain.CurtainRunTime)
        self.myApp.MissionDataTime.setDisplayFormat(self.__appDataMgr.DataTimeFormat)
        self.myApp.MissionDataTime.setDateTime(self.myApp.GetSysDataTime())

        #start thread to  read smoke value



    # get and set
    def GetCurtain(self):
        return self.__curtain
    # web
    def WilddogCallBack(self,wilddogInfo):
        if self.__curtain.CurAction==Code.Curtain.CurtainManager.ActionType.Wait:
            wilddogCurtainPos = int(wilddogInfo['Curtain']['ControlValue'])
            if not wilddogCurtainPos==self.__curtain.Position:
                self.ControlCurtainWithTargetPos(wilddogCurtainPos)
            try:
                curMissionList = wilddogInfo['Curtain']['MissionList']
            except:
                pass
            else:
                # print(" curMissionList == self.__lastMissionList " + str(curMissionList == self.__lastMissionList))
                if not curMissionList == self.__lastMissionList:
                    self.__lastMissionList = curMissionList
                    curMissionTimeList = []
                    curTimeStamp = self.__timeMgr.GetSystemDataTimeStamp()
                    for time in self.__lastMissionList:
                        time = int(time)
                        if time - curTimeStamp < 10:
                            self.__wilddogMgr.DeleteWilddogNodeValue('Curtain/MissionList/' + str(time))
                        else:
                            curMissionTimeList.append(time)
                            if not self.missionList.__contains__(time):
                                self.missionList.append(time)
                                listItem = MyListItem(time, self.__lastMissionList[str(time)][self.__missionValueKey],
                                                      self)
                                self.myApp.ListWidget.addItem(listItem)
                                self.myApp.ListWidget.sortItems()
                    # index = 0
                    # while index < self.myApp.ListWidget.count():
                    #     mission = self.myApp.ListWidget.item(index)
                    #     missionTimeStamp = mission.targetTimeStamp
                    #     print(missionTimeStamp)
                    #     if not curMissionTimeList.__contains__(missionTimeStamp):
                    #         self.myApp.ListWidget.takeItem(mission)
                    #         self.missionList.remove(missionTimeStamp)
                    #     index += 1
                    # pass

    # UI Functions
    def OnSliderReleased(self):
        selectValue = self.myApp.CurtainPos.text()
        self.ControlCurtainWithTargetPos(selectValue)

    def ControlCurtainWithTargetPos(self,targetPos):
        self.__curtain.ControlCurtainWithTargetPos(int(targetPos))
        self.myApp.CurtainPos.setText(str(self.__curtain.Position))
        self.myApp.CurtainControlSlider.setValue(self.__curtain.Position)
        self.__wilddogMgr.UpdateWilddogNodeValue(self.__controlValueUrl, targetPos)

    def OnAddMissionClicked(self):
        self._missionOperationType = 0  # 0 is add operation 1 is remove operation
        self.myApp.AddMissionBtn.setEnabled(False)
        self.myApp.DeleteMissionBtn.setEnabled(False)
        self.myApp.ComfirmBtn.setEnabled(True)
        self.myApp.CancelBtn.setEnabled(True)
        self.myApp.MissionDataTime.setEnabled(True)
        self.myApp.MissionSlider.setEnabled(True)
    def OnDeleteMissionClicked(self):
        self._missionOperationType = 1  # 0 is add operation 1 is remove operation
        self.myApp.AddMissionBtn.setEnabled(False)
        self.myApp.DeleteMissionBtn.setEnabled(False)
        self.myApp.ComfirmBtn.setEnabled(True)
        self.myApp.CancelBtn.setEnabled(True)
    def OnConfirmBtnClicked(self):
        if(self._missionOperationType==0):
            if(self.AddMission()==False):
                return
        elif(self._missionOperationType==1):
            if(self.RemoveMission()==False):
                return
        print("OnConfirmBtnClicked")
        self.ResetMissionOperationPlane()
    def OnCancelBtnClicked(self):
        print("OnCancelBtnClicked")
        self.ResetMissionOperationPlane()
    def ResetMissionOperationPlane(self):
        self.myApp.MissionDataTime.setDateTime(self.myApp.GetSysDataTime())
        self.myApp.MissionValue.setText("0")
        self.myApp.MissionSlider.setValue(0)
        self.myApp.AddMissionBtn.setEnabled(True)
        self.myApp.DeleteMissionBtn.setEnabled(True)
        self.myApp.ComfirmBtn.setEnabled(False)
        self.myApp.CancelBtn.setEnabled(False)
        self.myApp.MissionDataTime.setEnabled(False)
        self.myApp.MissionSlider.setEnabled(False)

        # upload value

    # Mission Functions
    def AddMission(self):
        print("AddMission")
        selectDataTime = self.myApp.MissionDataTime.dateTime()
        selectTimeStamp = selectDataTime.toTime_t()
        if (selectTimeStamp in self.missionList):
            self.myApp.ShowTip(self.__appDataMgr.LocalizationMsg.AddMissionError, 3)
            return False
        sysTimeStamp = self.myApp.GetSysDataTime().toTime_t()
        waitTime = selectTimeStamp - sysTimeStamp
        if (waitTime < self.__appDataMgr.MissionIntervalTime):
            self.myApp.ShowTip(self.__appDataMgr.LocalizationMsg.AddMissionError, 3)
            return False
        else:
            self.__wilddogMgr.UpdateWilddogNodeValue(self.__missionListUrl + '/' + str(selectTimeStamp),
                                                     {self.__missionTimeKey: selectDataTime.toString(self.__appDataMgr.DataTimeFormat) ,self.__missionValueKey: self.myApp.MissionSlider.value()})
        return True

    def RemoveMission(self):
        print("RemoveMission")
        self.__wilddogMgr.DeleteWilddogNodeValue('Curtain/MissionList/' + str(self.myApp.ListWidget.currentItem().targetTimeStamp))
        curItem = self.myApp.ListWidget.currentRow()
        self.myApp.ListWidget.takeItem(curItem)
        return True

    # Curtain CallBack Function
    def OnCurtainReseting(self):
        print("OnCurtainReseting")
        self.myApp.CurtainControlSlider.setEnabled(False)
        self.myApp.CurtainState.setText(self.__appDataMgr.LocalizationMsg.CurtainResetTipStr)

    def OnCurtainStart(self):
        print("OnCurtainStart")
        self.myApp.CurtainControlSlider.setEnabled(False)

    def OnCurtainStop(self):
        print("OnCurtainStop")
        self.myApp.CurtainState.setText(self.__appDataMgr.LocalizationMsg.CurtaionStopTipStr)
        self.myApp.CurtainControlSlider.setEnabled(True)

    def OnCurtainPosUpdate(self,pos):
        # print("OnCurtainPosUpdate"+str(pos))
        self.myApp.CurtainState.setText(self.__appDataMgr.LocalizationMsg.CurtaionRunningTipStr+str(self.__curtain.Position))
        self.myApp.CurtainControlSlider.setValue(self.__curtain.Position)
        self.myApp.CurtainPos.setText(str(pos))



class MyListItem(QtGui.QListWidgetItem):
    def __init__(self,targetTimeStamp,targetPos,MyCurtainModule):
        self.__curtainModule = MyCurtainModule
        self.__myApp = self.__curtainModule.myApp
        self.targetPos = targetPos
        targetTime = datetime.datetime.fromtimestamp(targetTimeStamp)
        self.targetTimeStamp = targetTimeStamp
        self.timer = QTimer()
        self.timer.timeout.connect(self.TimerCallBack)
        QtGui.QListWidgetItem.__init__(self, str(targetTime)+ "      TargetPos : " + str(self.targetPos))
        self.timer.start((self.targetTimeStamp - self.__myApp.GetTimeMgr().GetSystemDataTimeStamp())*1000)

    def __del__(self):
        print("MyListItem __del__")
        if (self.targetTimeStamp in   self.__curtainModule.missionList):
            self.__curtainModule.missionList.remove(self.targetTimeStamp)
        if (self.timer.isActive()):
            self.timer.stop()

    def TimerCallBack(self):
        self.ControlCurtain()
        self.__myApp.ListWidget.takeItem(self.__myApp.ListWidget.row(self))
        self.__myApp.GetWilddogMgr().DeleteWilddogNodeValue('Curtain/MissionList/' + str(self.targetTimeStamp))
    def ControlCurtain(self):
        self.__curtainModule.ControlCurtainWithTargetPos(self.targetPos)


