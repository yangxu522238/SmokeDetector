# -*- coding: utf-8 -*-

from PyQt4 import  QtGui
from PyQt4.QtCore import QTimer
from enum import Enum

class Curtain(QtGui.QMainWindow):
    def __init__(self,MainWindow,runtime):
        QtGui.QMainWindow.__init__(self)
        self.Position =0 # Curtain positon

        self.CurAction = ActionType.Wait
        self.CurtainRunTime = runtime  # The time the curtain is all open
        self.MainWindow=MainWindow
        # init timer
        self.RunningTimer = QTimer(self) # update curtain position
        self.RunningTimer.setInterval(1000)
        self.RunningTimer.timeout.connect(self.OnCurtainRunning)

        self.CommandTimer=QTimer(self)# wait time do command
        self.CommandTimer.setSingleShot(True)
        self.CommandTimer.timeout.connect(self.StopCurtain)

        # CallBack Properties
        self.CommandStartCallBack=[]
        self.CommandStopCallBack=[]
        self.CommandRunningCallBack=[]
        self.CurtainResetingCallBack=[]

    # Curtain Action
    def ControlCurtainWithTargetPos(self,targetPos):
        print("ControlCurtainWithTargetPos" + str(targetPos)+" selfPosition: " + str(self.Position))
        waitTime = (targetPos - self.Position) * 1000
        print("ControlCurtainWithTargetPos waitTime :" + str(waitTime))
        if (waitTime == 0):
            return
        elif (waitTime < 0):
            self.OpenCurtain(abs(waitTime))
        else:
            self.CloseCurtain(abs(waitTime))


    def ResetCurtain(self):
        print("ResetCurtain")
        self.CurAction=ActionType.Reset
        self.Position = 0
        self.DoCurtainResetingCallBack()
        self.CloseCommand()
        self.CommandTimer.start(self.CurtainRunTime*1000)

    def OpenCurtain(self,openLevel):
        print("OpenCurtain"+str(openLevel))
        if(self.CurAction==ActionType.Reset):
            return
        self.CurAction = ActionType.Open
        self.DoCommandStartCallBack()
        self.StopAllTimers() # Stop all timers
        self.RunningTimer.start()
        self.OpenCommand()
        self.CommandTimer.start(openLevel)



    def CloseCurtain(self,closelevel):
        print("CloseCurtain"+str(closelevel))
        if (self.CurAction == ActionType.Reset):
            return
        self.CurAction = ActionType.Close
        self.DoCommandStartCallBack()
        self.StopAllTimers() # Stop all timers
        self.RunningTimer.start()
        self.CloseCommand()
        self.CommandTimer.start(closelevel)

    def StopCurtain(self):
        self.OnCurtainRunning()
        print("StopCurtain" + str(self.Position))
        self.CurAction = ActionType.Wait
        self.DoCommandStopCallBack()
        self.StopCommand()
        self.StopAllTimers()


    def OnCurtainRunning(self):
        print("OnCurtainRunning")
        if(self.CurAction==ActionType.Open and self.Position >0):
            self.Position -= 1
        elif(self.CurAction==ActionType.Close and self.Position < self.CurtainRunTime):
            self.Position += 1
        self.DoCammandRunningCallBack()


    # StopAllTimers
    def StopAllTimers(self):
        if (self.CommandTimer.isActive()):
            self.CommandTimer.stop()
        if (self.RunningTimer.isActive()):
            self.RunningTimer.stop()

    # CallBack Functions
    def DoCommandStartCallBack(self):
        for callback in self.CommandStartCallBack:
            callback()
    def DoCommandStopCallBack(self):
        for callback in self.CommandStopCallBack:
            callback()
    def DoCammandRunningCallBack(self):
        for callback in self.CommandRunningCallBack:
            callback(self.Position)

    def DoCurtainResetingCallBack(self):
        for callback in self.CurtainResetingCallBack:
            callback()


    # Curtain Command Functions

    def OpenCommand(self):
        self.MainWindow.GetIOMgr().WriteToFile(self.MainWindow.GetIOPath(),str(ActionType.Open.value))

    def CloseCommand(self):
        self.MainWindow.GetIOMgr().WriteToFile(self.MainWindow.GetIOPath(),str(ActionType.Close.value))

    def StopCommand(self):
        self.MainWindow.GetIOMgr().WriteToFile(self.MainWindow.GetIOPath(),str(ActionType.Stop.value))

class ActionType(Enum):
    Wait  = -1
    Reset = 100
    Open  = 0
    Close = 1
    Stop  = 2