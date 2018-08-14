# -*- coding: utf-8 -*-
import  os


class DataMsg(object):
    def __init__(self,is_En=True):
        self.DataFormat = "yyyy-MM-dd"
        self.TimeFormat = "hh:mm:ss"
        self.DataTimeFormat = "yyyy-MM-dd hh：mm：ss"
        self.WilddogLoopTimer = 3
        self.MissionIntervalTime = 60

        self.WilddofUrl = "https://wd6711391518tgqjft.wilddogio.com/Flagmingo/Curtain/MissionList.json"

        self.TestIOFilePath = os.path.dirname(os.path.realpath(__file__)) + "testFile.txt"
        self.IOFilePath = "/sys/bus/platform/drivers/machine/soc:machine/value"

        if(is_En):
            self.LocalizationMsg = self.En_DataMsg()
        else:
            self.LocalizationMsg = self.Ch_DataMsg()
    pass
    class Ch_DataMsg():
        def __init__(self):
            self.AddMissionError = "添加任务失败，请重新选择任务"
            self.CurtainResetTipStr = "应用初始化中请等待..."
            self.CurtaionStopTipStr = "窗帘已停止移动...等待命令.."
            self.CurtaionRunningTipStr = "窗帘运行中,当前位置： "
            self.ControlSliderOperationTipStr = "调整滑块控制窗帘位置,左端为窗帘关闭,右端为窗帘完全打开"
            self.MissionTitleStr = "当前任务列表"
            self.AddMissionBtnStr = "添加"
            self.DeleteMissionBtnStr = "删除"
            self.ComfirmBtnStr = "确认"
            self.CancelBtnStr = "取消"
            self.LightBtnTextClosed = "打开"
            self.LightBtnTextOpened = "关闭"
            self.LightTipTextClosed="当前灯光处于关闭状态，点击按钮打开灯光"
            self.LightTipTextOpened = "当前灯光处于打开状态，点击按钮关闭灯光"
    class En_DataMsg():
        def __init__(self):
            self.AddMissionError = "Failed to add task, please reselect task !"
            self.CurtainResetTipStr = "Please wait for application initialization..."
            self.CurtaionStopTipStr = "The curtain has stopped moving... waiting for the command:"
            self.CurtaionRunningTipStr = "The curtain is running, current position: "
            self.ControlSliderOperationTipStr = "Adjust the slider to control the position of the curtain"
            self.MissionTitleStr = "Current task list"
            self.AddMissionBtnStr = "Add"
            self.DeleteMissionBtnStr = "Remove"
            self.ComfirmBtnStr = "Confirm"
            self.CancelBtnStr = "Cancel"
            self.LightBtnTextClosed = "Open"
            self.LightBtnTextOpened = "Close"
            self.LightTipTextClosed = "The current light is off, click the button to turn on the light"
            self.LightTipTextOpened = "The current light is on, click the button to turn off the light"








