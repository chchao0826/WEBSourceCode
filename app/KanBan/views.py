# -*-coding:utf-8-*-
from . import KanBan
from flask import render_template, Flask, request

from app.KanBan.Models.DX import DXKanBanData, DXKanBanChartData
from app.KanBan.SQLExec.EquipmentService import equipmentServiceData
from app.KanBan.SQLExec.FloorPlan import emStatus, StoreStatus, wpStatus
from app.KanBan.SQLExec.JSInformation import JSData
from app.Plan.Models.plan import GetEquipment
from app.PlanDye.SQLExec.Dyeing import DyeingData, DyeingEquipment, IDGetData, IDGetEquipment, searchValue

import json


# 主页
@KanBan.route('/')
def index():
    return render_template('KanBan/base.html')


# 工厂平面图
@KanBan.route('/floorplan/')
def floorPlan():
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

    return render_template('KanBan/floorPlan.html', TJ_eq=TJ_eq, MM_eq=MM_eq, Dye_eq1=Dye_eq1, Dye_eq2=Dye_eq2, Dye_eq3=Dye_eq3, Dye_eq4=Dye_eq4, Dye_eq5=Dye_eq5, Dye_eq6=Dye_eq6, PB_eq=PB_eq, DB_eq=DB_eq, TS_eq=TS_eq, FB_eq=FB_eq, SX_eq=SX_eq, DX_eq1=DX_eq1, DX_eq2=DX_eq2, DJ_eq=DJ_eq, YB_eq=YB_eq, TJ_WIP=TJ_WIP, SX_WIP=SX_WIP, YD_WIP=YD_WIP, Dye_WIP=Dye_WIP, DX_WIP=DX_WIP, YB_WIP=YB_WIP, DJ_WIP=DJ_WIP, FP=FP, STA=STA, STC=STC)


# 技术部看板
@KanBan.route('/JS/')
def JSInformation():
    cardData = []
    returnData = JSData()
    print(returnData)
    for i in returnData[0]:
        if i['nPageNumber'] == 1:
            cardData.append(i)
    print('----------------')

    # cardData = returnData[0]
    salesGroupList = returnData[1]
    nPage = returnData[8]
    return render_template('KanBan/JSInformation.html', returnData=cardData, salesGroupList=salesGroupList, nPage=nPage)


# AJAX
@KanBan.route('/JS/AJAX/sSaleGroupName2/<GetValue>')
def JSDataAJAX(GetValue):
    print('-----------------')
    print(GetValue)
    sSaleGroupName = ''
    nPage = 1
    if GetValue.find('_') == -1:
        sSaleGroupName = GetValue
    else:
        sSaleGroupName = GetValue.split('_')[0]
        nPage = GetValue.split('_')[1]
    print(sSaleGroupName)
    print(nPage)

    returnData = JSData(sSaleGroupName)[0]
    nReturnPage = JSData(sSaleGroupName)[8]
    returnHTML = ''

    for i in returnData:

        if str(nPage) == str(i['nPageNumber']):

            returnHTML += '\
                <div class="col-md-4" style="height:400px; margin-top: -7px; margin-bottom: 30px;" onclick="turnOver()"> \
                    <div class="box direct-chat" style="height:400px; border: 6px solid %s;"> \
                        <div class="box-header text-center"> \
                            <h3 class="box-title" style="font-size: 55px; font-weight: 900;">%s</h3> \
                        </div> \
                        <div class="box-body" style="margin-top:-8px; height: 350px;"> \
                            <div class="direct-chat-messages" style="height: 350px;"> \
                                <ul class="text-center" style="font-size : 55px; font-weight: 700;"> \
                                    <li>%s</li> \
                                    <li>%s</li> \
                                    <li>%s</li> \
                                    <li>%s</li> \
                                </ul> \
                            </div> \
                            <div class="direct-chat-contacts" style="font-size: 30px; height:350px;" name="remark"> \
                                %s \
                            </div> \
                        </div> \
                    </div> \
                </div>' % (i['borderColor'], i['sMaterialNo'], i['sCardNo'], i['tCardTime'], i['sWorkingProcedureName'], i['sSalesName'], i['sKanBanRemark'])

    returnHTML += '<div class="fixed" id="fixed"> \
                    <nav aria-label="Page navigation"> \
                        <ul class="pagination" style="height:10px; margin-top:-4px;">'
    for i in range(1, nReturnPage + 1):
        # print(i)
        # print(nPage)
        if str(i) == str(nPage):
            returnHTML += '<li class="active"><a href="#" onclick="clickPage(%s)" id="%s" style="font-size: 20px;">%s</a></li>' % (
                i, i, i)
        else:
            returnHTML += '<li><a href="#" onclick="clickPage(%s)"  id="%s" style="font-size: 20px;">%s</a></li>' % (
                i, i, i)

    returnHTML += '</ul> \
                </nav> \
            </div> \
            <script>PageCenter()</script>'

    print('++++++++++++++++')
    print(returnHTML)
    returnHTML += '<script>scroll();</script>'
    return returnHTML


# AJAX 头部标题
@KanBan.route('/JS/AJAXHEADER')
def JSDataAJAXHeader():
    returnData = JSData()[1]
    returnHtml = '<ul class="nav nav-pills nav-justified " style="background-color:#F5F5F5;" id="GroupUL">'
    for i in returnData:
        returnHtml += '\
            <li role="presentation" name="liNav" style="font-size:25px;"> \
                <a href="#" onclick="onclickGroup()"> \
                    <span>%s</span> \
                    <span data-toggle="tooltip" title="3 New Messages" class="badge bg-yellow" style="font-size:20px; margin-top:-5px; border-radius:20px;"> %s </span> \
                </a> \
            </li>' % (i['sSalesGroupName'], i['nCount'])
    returnHtml += '</ul>'
    return returnHtml


# AJAX Title 营业部门 转至 业务员
@KanBan.route('/JS/AJAX/sSaleGroupName/<sSaleGroupName>')
def JSDataAJAXSalesGroup(sSaleGroupName):
    sSalesGroupName_2 = ''
    if sSaleGroupName == 'YF':
        sSalesGroupName_2 = '研发处'
    elif sSaleGroupName == 'TFKF':
        sSalesGroupName_2 = '研发处开发'
    elif sSaleGroupName == 'Y2':
        sSalesGroupName_2 = '营二处'
    elif sSaleGroupName == 'Y3':
        sSalesGroupName_2 = '营三处'

    returnData = JSData(sSalesGroupName_2)[3]
    returnHtml = '<ul class="nav nav-pills nav-justified " style="background-color:#F5F5F5;" id="GroupUL">'
    for i in returnData:
        returnHtml += '\
            <li role="presentation" name="liNav" style="font-size:25px;"> \
                <a href="#" onclick = "onclickSale()"> \
                <span> %s </span> \
                <span data-toggle="tooltip" title="3 New Messages" class="badge bg-yellow" style="font-size:20px; margin-top:-5px; border-radius:20px;"> %s </span> \
                </a> \
            </li>' % (i['sSalesName'], i['nSaleCount'])
    returnHtml += '\
            <li role="presentation" name="liNav" style="font-size:25px;"> \
                <a href="#" onclick="updateGroup()"> \
                <span> 返回上级 </span> \
                </a> \
            </li> \
        </ul>'
    return returnHtml


# AJAX Title 业务员 更新 wrapper
@KanBan.route('/JS/AJAX/sSalesName2/<sSaleName>')
def JSDateAJAXSale2(sSaleName):
    returnData = JSData(sSaleName)[4]
    returnHTML = ''
    # print('-----------------')
    for i in returnData:
        returnHTML += '\
            <div class="col-md-4" style="height:400px;" onclick="turnOver()"> \
                <div class="box direct-chat" style="height:400px; border-top: 6px solid %s"> \
                    <div class="box-header text-center"> \
                        <h3 class="box-title" style="font-size: 60px; font-weight: 900;">%s</h3> \
                    </div> \
                    <div class="box-body" style="margin-top:-8px; height: 350px;"> \
                        <div class="direct-chat-messages" style="height: 350px;"> \
                            <ul class="text-center" style="font-size:50px; font-weight: 500;"> \
                                <li>%s</li> \
                                <li>%s</li> \
                                <li>%s</li> \
                                <li>%s</li> \
                            </ul> \
                        </div> \
                        <div class="direct-chat-contacts" style="font-size: 50px; height:350px;" name="remark"> \
                            %s \
                        </div> \
                    </div> \
                </div> \
            </div>' % (i['borderColor'], i['sMaterialNo'], i['sCardNo'], i['tCardTime'], i['sWorkingProcedureName'], i['sSalesName'], i['sKanBanRemark'])
    returnHTML += '<script>scroll();</script>'
    return returnHTML


# AJAX Title 业务员 更新 wrapper + 循环
@KanBan.route('/JS/AJAX/sSalesName/<sSaleName>')
def JSDateAJAXSale(sSaleName):
    # print('11111')
    returnData = JSData(sSaleName)[4]
    # print(sSaleName)
    returnHTML = ''
    # print(returnData)
    for i in returnData:
        returnHTML += '\
            <div class="col-md-2" style="height:400px;"> \
                <div class="box direct-chat" style="height:400px; border-top: 6px solid %s"> \
                    <div class="box-header text-center"> \
                        <h3 class="box-title" style="font-size: 60px; font-weight: 900;">%s</h3> \
                    </div> \
                    <div class="box-body" style="margin-top:-8px; height: 350px;"> \
                        <div class="direct-chat-messages" style="height: 350px;"> \
                            <ul class="text-center" style="font-size:50px; font-weight: 500;"> \
                                <li>%s</li> \
                                <li>%s</li> \
                                <li>%s</li> \
                                <li>%s</li> \
                            </ul> \
                        </div> \
                        <div class="direct-chat-contacts" style="font-size: 50px; height:350px;" name="remark"> \
                            %s \
                        </div> \
                    </div> \
                </div> \
            </div>' % (i['borderColor'], i['sMaterialNo'], i['sCardNo'], i['tCardTime'], i['sWorkingProcedureName'], i['sSalesName'], i['sKanBanRemark'])
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


# 技术部工段
@KanBan.route('/JS/sWorkingProcedureName/')
def JSPro():
    # print('12222')
    returnData = JSData()
    cardData = []
    for i in returnData[0]:
        if i['nPageNumber'] == 1:
            cardData.append(i)
    workingProcedureList = returnData[9]
    nPage = returnData[8]
    return render_template('kanban/JSWorkingProcedure.html', returnData=cardData, workingProcedureList=workingProcedureList, nPage=nPage)


# 定型看板
@KanBan.route('/DX/')
def DXKanBan():
    returnData = DXKanBanData()
    EqList = GetEquipment('整理')
    print(returnData)
    print(EqList)
    return render_template('KanBan/plan_zl.html', returnData=returnData, equipmentData=EqList)


# 定型看板-山积图
@KanBan.route('/DX/chart')
def DXKanBan_Chart():
    EqList = GetEquipment('整理')
    DXKanBanChart = DXKanBanChartData()
    print(EqList)
    print('================')
    print(DXKanBanChart)
    return render_template('kanban/plan_zl_chart.html', EqList=EqList, DXKanBanChart=DXKanBanChart)


# 故障检修看板
@KanBan.route('/service')
def equipmentService():
    returnData = equipmentServiceData()
    return render_template('KanBan/equipmentService.html', returnData=returnData[0], nCount=returnData[1], nAllPage=returnData[2])


# 故障看板点击页码
@KanBan.route('/service/page/<nPage>')
def ServiceAJAXPage(nPage):
    returnData = equipmentServiceData(nPage)[0]
    returnHTML = ''
    print(returnData)
    for i in returnData:
        print('================')
        print(i)
        returnHTML += '\
            <div class="col-md-2 col_style"> \
                <ul class="ul_style"> \
                    <li> \
                        <div class="circle" style="background-color: %s;"></div> \
                    </li> \
                    <li class="col_title"> \
                        <span>%s单</span> \
                    </li> \
                    <li> \
                        <div style="border-top: 2px dashed #111;"></div> \
                    </li> \
                    <li> \
                        <span>%s</span> \
                        <span> - </span> \
                        <span>%s</span> \
                    </li> \
                    <li> \
                        <span>%s</span> \
                    <li> \
                        <span>%s</span> \
                        <span> - </span> \
                        <span>%s</span> \
                    <li style="height:70px;"> \
                        <span>%s</span> \
                    </li> \
                    <li> \
                        <div style="border-top: 2px solid #111;"></div> \
                    </li> \
                    <li> \
                        <span>受理人员:</span> \
                        <span>%s</span> \
                    </li> \
                    <li> \
                        <span>目前状态:</span> \
                        <span>%s</span> \
                    </li> \
                    <li> \
                        <span>%s</span> \
                    </li> \
                </ul> \
            </div>' % (i['sStatus'], i['sServiceType'], i['sWorkCentreName'], i['sReportName'], i['sEquipmentNo'], i['sEquipmentDetailType'], i['sEquipmentDetail'], i['sFaultReason'], i['sServiceName'], i['sServiceStatus'], i['sTime'])
    return returnHTML


# 染色看板-业务
@KanBan.route('/PlanDye/sale')
def PlanDyeSale():
    return render_template('KanBan/planDye_sale.html')


# AJAX 得到点击的机台的信息
@KanBan.route('/PlanDye/AJAX/Data/<equipmentNo>')
def Equipment(equipmentNo):
    ID = equipmentNo.split('_')[1]
    returnData = IDGetData(ID)
    returnEquipment = IDGetEquipment(ID)
    returnHTML = ''

    for i in returnEquipment:
        returnHTML += ' <ul class="slot-list" id="Eq_%s"> \
                            <div> \
                                <input class="title_var" type="text" readOnly="true" value=%s> \
                                <span class="input-group-addon title_span_var" style="background-color:#FFFF00; width:1250px; font-size: 12px;" id="basic-addon1">%s</span> \
                                <span class="input-group-addon title_span_var" style="background-color:#FFFF00; width:1250px; font-size: 12px;" id="basic-addon1">共: %s 卡</span> \
                            </div>' % (i['ID'], i['sEquipmentNo'], i['sEquipmentName'], i['nCardCount'])

    for i in returnData:
        if i['sType'] == '洗缸':
            returnHTML += '\
                <li class="slot-item XG_li" id="Card_%s"> \
                    <div class="clearfix XG_div"> \
                        <div> \
                            <div> \
                                <span>洗缸</span> \
                            </div> \
                            <div> \
                                <span></span> \
                            </div> \
                        </div> \
                    </div> \
                </li>' % (i['ID'])
        else:
            returnHTML += ' \
                    <li class="slot-item li_style" id="Card_%s" \
                        style="border-left:10px solid %s; border-right:10px solid %s; "> \
                        <div class="clearfix"> \
                            <div class="float_left left_div border_right"> \
                                <div type="text" class="left_1 hover border_bottom" style="background-color: %s;"> \
                                    <span>%s</span> \
                                </div> \
                                <div class="left_2 border_bottom"> \
                                    <span>%s</span> \
                                </div> \
                                <div class="left_3 border_bottom"> \
                                    <span>%s</span> \
                                </div> \
                            </div> \
                            <div class="float_left right_div"> \
                                <div class="right_1 border_bottom border_right float_left right_1_left" style="background-color: %s; "> <span>预</span> </div> \
                                <div class="right_1 border_bottom border_right float_left right_1_mid" style="background-color: %s; "> <span>化</span> </div> \
                                <div class="right_1 border_bottom border_right float_left right_1_right" style="background-color:%s"> <span>%s</span> </div> \
                                <div class="right_2 border_bottom"> <span>投胚: %s</span> </div> \
                                <div class="right_3 border_bottom" > <span>滞留: %s</span> </div> \
                                <div class="right_4 border_bottom"> \
                                    <span>%s</span> \
                                </div> \
                            </div> \
                            <div class="left_4"> \
                                <span>%s --> %s --> %s</span> \
                            </div> \
                        </div> \
                    </li> ' % (i['ID'], i['sWorkCode'], i['sColorCode'], i['bISCheck'], i['sCardNo'], i['sMaterialNo'], i['sColorNo'], i['sPSColor'], i['sIsHYS'], i['sDyeingColor'], i['sDyeingCount'], i['nFactInputQty'], i['sOverTime'], i['sCustomerName'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'])
    returnHTML += '</ul>'

    print(returnHTML)
    return returnHTML


# AJAX 点击机台组别更新机台号
@KanBan.route('/PlanDye/AJAX/equipment/<equipmentNo>', methods=['GET', 'POST'])
def AjaxData(equipmentNo):
    print(equipmentNo)
    getEuqList = DyeingEquipment(equipmentNo)
    returnHTML = ''
    nLength = str(round(99 / len(getEuqList), 2)) + '%'
    for i in getEuqList:
        returnHTML += '<li id="equ_%s" style="width: %s"><a onclick="btnEqui(\'equ_%s\')">%s</a></li>' % (
            i['ID'], nLength, i['ID'], i['sEquipmentNo'])

    return returnHTML
