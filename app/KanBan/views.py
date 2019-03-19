# -*-coding:utf-8-*-
from . import KanBan
from flask import render_template, Flask, request
from app.views.KanBan import emStatus, wpStatus, StoreStatus, DyeGetSample, JSData


import json

# 主页
@KanBan.route('/')
def index():
    return render_template('KanBan/base.html')

# 工厂平面图
@KanBan.route('/工厂平面图/')
def FloorPlan():
    statusVar = emStatus()
    WIP = wpStatus()
    # print(StoreStatus())
    STStore = StoreStatus()
    FP = STStore[0]
    STA = STStore[1]
    STC = STStore[2]

    TJ_WIP = WIP[0]
    SX_WIP = WIP[1]
    YD_WIP = WIP[2]
    Dye_WIP = WIP[3]
    DX_WIP = WIP[4]
    YB_WIP = WIP[4]
    DJ_WIP = WIP[4]
    # print(SX_WIP)
    # print(TJ_WIP)
    # print(statusVar)
    TJ_eq = statusVar[0]
    MM_eq = statusVar[1]
    Dye_eq1 = statusVar[2]
    # print(Dye_eq1)
    Dye_eq2 = statusVar[3]
    # print(Dye_eq2)
    Dye_eq3 = statusVar[4]
    # print(Dye_eq3)
    Dye_eq4 = statusVar[5]
    # print(Dye_eq4)
    Dye_eq5 = statusVar[6]
    # print(Dye_eq5)
    Dye_eq6 = statusVar[7]
    # print(Dye_eq6)
    PB_eq = statusVar[8]
    DB_eq = statusVar[9]
    TS_eq = statusVar[10]
    FB_eq = statusVar[11]
    SX_eq = statusVar[12]
    DX_eq1 = statusVar[13]
    DX_eq2 = statusVar[14]
    DJ_eq = statusVar[15]
    YB_eq = statusVar[16]

    return render_template('KanBan/FloorPlan.html', TJ_eq = TJ_eq, MM_eq = MM_eq, Dye_eq1 = Dye_eq1, Dye_eq2 = Dye_eq2, Dye_eq3 = Dye_eq3, Dye_eq4 = Dye_eq4, Dye_eq5 = Dye_eq5, Dye_eq6 = Dye_eq6, PB_eq = PB_eq, DB_eq = DB_eq, TS_eq = TS_eq, FB_eq = FB_eq, SX_eq = SX_eq, DX_eq1 = DX_eq1, DX_eq2 = DX_eq2, DJ_eq = DJ_eq, YB_eq = YB_eq, TJ_WIP = TJ_WIP, SX_WIP = SX_WIP, YD_WIP = YD_WIP, Dye_WIP = Dye_WIP, DX_WIP = DX_WIP, YB_WIP = YB_WIP, DJ_WIP = DJ_WIP, FP = FP, STA = STA, STC = STC)

# 取样看板
@KanBan.route('/取样/')
def GetSample():
    sVar = DyeGetSample()
    euipmentList = sVar[1]
    minList = sVar[5]
    print(minList)

    return render_template('KanBan/GetSample.html',euipmentList = euipmentList, minList = minList)

# 取样看板机台信息更新
@KanBan.route('/取样/AJAX')
def GetSampleAJAX():
    print('++++++'*12)
    sVar = DyeGetSample()
    euipmentList = sVar[1]
    AJAXData = ''
    for var in euipmentList:
        AJAXData += '<div class="all-mac-list text-center border-bottom "><span>%s</span></div>' % (var['sEuipmentNo'])
    return AJAXData

# 取样看板按照机台更新信息
@KanBan.route('/取样/AJAX/<sEquipmentNo>/')
def GetSampleEquipment(sEquipmentNo):
    # print('2222222222222222222')
    sVar = DyeGetSample(sEquipmentNo)
    activeList = sVar[2]
    # print(activeList)
    # print(prevList)
    # print(nextList)
    activeStr = ''
    for i in activeList:
        activeStr +='\
        <div class="left-top-div border-bottom" > \
            <div class="float-left inner-left border-right text-center font-color"> \
                <div class="mac-font border-bottom"> \
                    <span> %s </span> \
                </div> \
                <div class="card-font border-bottom text-center"> \
                    <span> %s </span> \
                </div> \
                <div class="cust-font text-center"> \
                    <span> %s </span> \
                </div> \
            </div> \
            <div class="float-left inner-right"> \
                <div class="top-top border-bottom font-color text-center"> \
                    <span> %s </span> \
                </div> \
                <div class="top-top border-bottom font-color text-center"> \
                    <span> %s </span> \
                </div> \
                <div class="top-top border-bottom font-color text-center"> \
                    <span>重量:</span> \
                    <span> %s </span> \
                </div> \
                <div class="top-bottom text-center font-color"> \
                    <span> %s </span> \
                </div> \
            </div> \
        </div> \
        <audio src= "/static/KanBan/audio/%s.mp3" style="display:none" id="audio"></audio> \
        <script> \
            getScreen(); \
            document.getElementById(\'audio\').play()\
        </script>'%(i['sEquipmentNo'], i['sCardNo'], i['sCustomerName'], i['sMaterialNo'], i['sColorNo'], i['nFactInputQty'], i['sRemark'], i['sEquipmentNo'])

             
    return activeStr

# 技术部看板
@KanBan.route('/技术部/')
def JSInformation():
    returnData = JSData()
    # print(returnData2)
    cardDate = returnData[0]
    salesGroupList = returnData[1]
    return render_template('KanBan/JSInformation.html',returnData = cardDate, salesGroupList = salesGroupList)

# AJAX
@KanBan.route('/技术部/AJAX/<sSaleGroupName>')
def JSDataAJAX(sSaleGroupName):
    returnData = JSData(sSaleGroupName)[2]
    returnHTML = ''
    # print(returnData)
    for i in returnData:
        print(i)
        returnHTML +='\
            <div class="col-md-3 float-left" id="{{i}}"> \
                <div class="box-primary border-top"> \
                    <div class="font text-center"> \
                        <ul name="ul1"> \
                            <li>%s</li> \
                            <li>%s</li> \
                            <li>%s</li> \
                            <li>%s</li> \
                            <li>%s</li> \
                        </ul> \
                    </div> \
                </div> \
            </div>'%(i['sCardNo'], i['sMaterialNo'], i['tCardTime'], i['sWorkingProcedureName'], i['sSalesName'])
    returnHTML += '<script>scroll();</script>'
    return returnHTML

# AJAX 头部标题
@KanBan.route('/技术部/AJAXHEADER')
def JSDataAJAXHeader():
    returnData = JSData()
    print(returnData)
    print('121211')
    # return 123



