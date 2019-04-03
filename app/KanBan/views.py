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
    return render_template('KanBan/GetSample.html',euipmentList = euipmentList, minList = minList)

# 取样看板机台信息更新
@KanBan.route('/取样/AJAX')
def GetSampleAJAX():
    sVar = DyeGetSample()
    euipmentList = sVar[1]
    AJAXData = ''
    for var in euipmentList:
        AJAXData += '<div class="all-mac-list text-center border-bottom " style="color:%s"><span>%s</span></div>' % (var['sColor'],var['sEuipmentNo'])
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
                    <span>%s</span> \
                    <sapn>%smin</span> \
                </div> \
            </div> \
        </div> \
        <audio src= "/static/KanBan/audio/Equipment/%s.mp3" style="display:none" id="audio1"></audio> \
        <script> \
            getScreen(); \
            var sVar = \"%s\"; \
            var voide11 = voide1(sVar); \
            var voide22 = voide2(sVar); \
            console.log(voide11); \
            console.log(voide22); \
            var voideSrc = "/static/KanBan/audio/"+ voide11 + voide22 +".mp3"; \
            console.log(voideSrc); \
            var aud = document.getElementById(\'audio1\'); \
            aud.play(); \
            aud.onended = function(){ \
                aud.src = voideSrc; \
                aud.play(); \
                aud.onended = function(){ \
                    return; \
                } \
            } \
        </script>'%(i['sEquipmentNo'], i['sCardNo'], i['sCustomerName'], i['sMaterialNo'], i['sColorNo'], i['nFactInputQty'], i['sType'], i['nNextCallTime'], i['sEquipmentNo'], i['sType'])

             
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
@KanBan.route('/技术部/AJAX/sSaleGroupName2/<sSaleGroupName>')
def JSDataAJAX(sSaleGroupName):
    returnData = JSData(sSaleGroupName)[2]
    returnHTML = ''
    # print(returnData)
    for i in returnData:
        # print(i)
        returnHTML +='\
            <div class="col-md-2" style="height:240px;"> \
                <div class="box direct-chat" style="height:220px; border-top: 6px solid %s"> \
                    <div class="box-header text-center"> \
                        <h3 class="box-title" style="font-size: 30px; font-weight: 900;">%s</h3> \
                    </div> \
                    <div class="box-body" style="margin-top:-8px;"> \
                        <div class="direct-chat-messages"> \
                            <ul class="text-center" style="font-size:26px; font-weight: 500;"> \
                                <li>%s</li> \
                                <li>%s</li> \
                                <li>%s</li> \
                                <li>%s</li> \
                            </ul> \
                        </div> \
                        <div class="direct-chat-contacts" style="font-size: 30px; height:172px;" name="remark"> \
                            %s \
                        </div> \
                    </div> \
                </div> \
            </div>'%(i['borderColor'], i['sMaterialNo'], i['sCardNo'], i['tCardTime'], i['sWorkingProcedureName'], i['sSalesName'], i['sKanBanRemark'])
    returnHTML += '<script>scroll();</script>'
    return returnHTML

# AJAX 头部标题
@KanBan.route('/技术部/AJAXHEADER')
def JSDataAJAXHeader():
    returnData = JSData()[1]
    returnHtml ='<ul class="nav nav-pills nav-justified " style="background-color:#F5F5F5;" id="GroupUL">'
    for i in returnData:
        returnHtml += '\
            <li role="presentation" name="liNav" style="font-size:25px;"> \
                <a href="#" onclick="onclickGroup()"> \
                    <span>%s</span> \
                    <span data-toggle="tooltip" title="3 New Messages" class="badge bg-yellow" style="font-size:20px; margin-top:-5px; border-radius:20px;"> %s </span> \
                </a> \
            </li>'%(i['sSalesGroupName'], i['nCount'])
    returnHtml += '</ul>'
    return returnHtml

@KanBan.route('/技术部/AJAX/sSaleGroupName/<sSaleGroupName>')
def JSDataAJAXSalesGroup(sSaleGroupName):
    returnData = JSData(sSaleGroupName)[3]
    returnHtml ='<ul class="nav nav-pills nav-justified " style="background-color:#F5F5F5;" id="GroupUL">'
    for i in returnData:
        returnHtml += '\
            <li role="presentation" name="liNav" style="font-size:25px;"> \
                <a href="#" onclick = "onclickSale()"> \
                <span> %s </span> \
                <span data-toggle="tooltip" title="3 New Messages" class="badge bg-yellow" style="font-size:20px; margin-top:-5px; border-radius:20px;"> %s </span> \
                </a> \
            </li>'%(i['sSalesName'], i['nSaleCount'])
    returnHtml += '\
            <li role="presentation" name="liNav" style="font-size:25px;"> \
                <a href="#" onclick="updateGroup()"> \
                <span> 返回上级 </span> \
                </a> \
            </li> \
        </ul>' 
    return returnHtml

@KanBan.route('/技术部/AJAX/sSalesName2/<sSaleName>')
def JSDateAJAXSale2(sSaleName):
    returnData = JSData(sSaleName)[4]
    returnHTML = ''
    print('-----------------')
    for i in returnData:
        returnHTML +='\
            <div class="col-md-2" style="height:240px;"> \
                <div class="box direct-chat" style="height:220px; border-top: 6px solid %s"> \
                    <div class="box-header text-center"> \
                        <h3 class="box-title" style="font-size: 30px; font-weight: 900;">%s</h3> \
                    </div> \
                    <div class="box-body" style="margin-top:-8px;"> \
                        <div class="direct-chat-messages"> \
                            <ul class="text-center" style="font-size:26px; font-weight: 500;"> \
                                <li>%s</li> \
                                <li>%s</li> \
                                <li>%s</li> \
                                <li>%s</li> \
                            </ul> \
                        </div> \
                        <div class="direct-chat-contacts" style="font-size: 30px; height:172px;" name="remark"> \
                            %s \
                        </div> \
                    </div> \
                </div> \
            </div>'%(i['borderColor'], i['sMaterialNo'], i['sCardNo'], i['tCardTime'], i['sWorkingProcedureName'], i['sSalesName'], i['sKanBanRemark'])
    returnHTML += '<script>scroll();</script>'
    return returnHTML

@KanBan.route('/技术部/AJAX/sSalesName/<sSaleName>')
def JSDateAJAXSale(sSaleName):
    print('11111')
    returnData = JSData(sSaleName)[4]
    print(sSaleName)
    returnHTML = ''
    # print(returnData)
    for i in returnData:
        returnHTML +='\
            <div class="col-md-2" style="height:240px;"> \
                <div class="box direct-chat" style="height:220px; border-top: 6px solid %s"> \
                    <div class="box-header text-center"> \
                        <h3 class="box-title" style="font-size: 30px; font-weight: 900;">%s</h3> \
                    </div> \
                    <div class="box-body" style="margin-top:-8px;"> \
                        <div class="direct-chat-messages"> \
                            <ul class="text-center" style="font-size:26px; font-weight: 500;"> \
                                <li>%s</li> \
                                <li>%s</li> \
                                <li>%s</li> \
                                <li>%s</li> \
                            </ul> \
                        </div> \
                        <div class="direct-chat-contacts" style="font-size: 30px; height:172px;" name="remark"> \
                            %s \
                        </div> \
                    </div> \
                </div> \
            </div>'%(i['borderColor'], i['sMaterialNo'], i['sCardNo'], i['tCardTime'], i['sWorkingProcedureName'], i['sSalesName'], i['sKanBanRemark'])
        returnHTML += '\
            <script>\
                var second = 1; \
                window.setInterval("interval();",1000);\
                var interval = function() { \
                    second++; \
                    console.log(second); \
                    if (second == 60){ \
                        window.location.reload(); \
                    } \
                } \
                scroll(); \
            </script>'
    return returnHTML
    


