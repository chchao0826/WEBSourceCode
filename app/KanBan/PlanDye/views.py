# -*-coding:utf-8-*-
# 染色预排看板

from app.KanBan import KanBan
from flask import render_template, Flask, request
from app.Plan.Models.plan import GetEquipment
from app.PlanDye.SQLExec.Dyeing import DyeingData, DyeingEquipment, IDGetData, IDGetEquipment
from app.PlanDye.SQLExec.SplitArea import IDGetCheckData, IDGetAllData
from app.KanBan.PlanDye.SQLExec.Search import SearchExec

import json


# 染色看板-main
@KanBan.route('/PlanDye/main')
def PlanDyeMain():
    return render_template('KanBan_PlanDye/planDye_main.html')


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


# 染色看板-业务
@KanBan.route('/PlanDye/sale')
def PlanDyeSale():
    return render_template('KanBan_PlanDye/planDye_sale.html')


# AJAX 得到点击的机台的信息
@KanBan.route('/PlanDye/AJAX/SaleData/<equipmentNo>')
def SaleEquipment(equipmentNo):
    ID = equipmentNo.split('_')[1]
    print('====================')
    returnData = IDGetCheckData(ID)
    returnEquipment = IDGetEquipment(ID)
    returnHTML = ''

    for i in returnEquipment:
        returnHTML += ' <ul class="slot-list" id="Eq_%s"> \
                            <div> \
                                <input class="title_var" type="text" readOnly="true" value=%s> \
                                <span class="input-group-addon title_span_var" style="background-color:#FFFF00; width:1250px; font-size: 12px;" id="basic-addon1">%s</span> \
                                <span class="input-group-addon title_span_var" style="background-color:#FFFF00; width:1250px; font-size: 12px;" id="basic-addon1">共: %s 卡</span> \
                            </div>' % (i['ID'], i['sEquipmentNo'], i['sEquipmentName'], i['nCheckCount'])

    for i in returnData:
        if str(i['sType']).find('洗缸') != -1:
            returnHTML += '\
                <li class="slot-it em XG_li" id="Card_%s"> \
                    <div class="clearfix XG_div"> \
                        <div> \
                            <div> \
                                <span>%s</span> \
                            </div> \
                            <div> \
                                <span></span> \
                            </div> \
                        </div> \
                    </div> \
                </li>' % (i['ID'], i['sType'])
        else:
            returnHTML += ' \
                            <li class="slot-item li_style" id="Card_%s" style="background-color: %s"> \
                                <div class="float_left border_div" style="background-color: %s;"></div> \
                                <div class="left_div float_left border_right"> \
                                    <ul> \
                                        <li class="border_bottom left_span_li"><span>%s</span></li> \
                                        <li class="border_bottom left_span_li"><span>%s</span></li> \
                                        <li class="border_bottom left_span_li"><span>%s</span></li> \
                                        <li class="border_bottom left_span_li"><span>%s</span></li> \
                                        <li class="border_bottom left_work_li"><span>%s --&gt; %s --&gt; %s</span></li> \
                                    </ul> \
                                </div> \
                                <div class="right_div float_left border_right"> \
                                    <ul> \
                                        <li class="border_bottom right_span_li"><span>%s</span></li> \
                                        <li class="border_bottom right_span_li"><span>投胚:%s</span></li> \
                                        <li class="border_bottom right_span_li"><span>超时:%s</span></li> \
                                        <li class="border_bottom color_li"><span>%s</span></li> \
                                        <li class="border_bottom right_work_li"><span>%s</span></li> \
                                    </ul> \
                                </div> \
                                <div class="float_left border_div" style="background-color: %s;"></div> \
                            </li> \
                        ' % (i['ID'], i['sIsStart'], i['sWorkCode'], i['sOrderNo'], i['sCardNo'], i['sMaterialNo'], i['sColorNo'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['sSalesName'], i['nFactInputQty'], i['sOverTime'], i['sColorName'], i['tPlanTime'], i['sColorCode'])
    returnHTML += '</ul>'

    print(returnHTML)
    return returnHTML


# 搜索数据
@KanBan.route('/PlanDye/sale/Search/<inputValue>')
def SearchDataBase(inputValue):

    returnValue = SearchExec(inputValue, 1)
    returnList = returnValue[0]
    nPage = returnValue[1]

    return render_template('KanBan_PlanDye/PlanDye_choice.html', returnList=returnList, nPage=nPage)


# 搜索页面点击页码操作
@KanBan.route('/PlanDye/sale/Search/Page/<sUrlvalue>')
def SearchPage(sUrlvalue):
    sInputValue = sUrlvalue.split('_')[0]
    nPage = sUrlvalue.split('_')[1]
    returnValue = SearchExec(sInputValue, nPage)
    returnHTML = '\
        <tbody> \
            <tr> \
                <th>订单号</th> \
                <th>工卡号</th> \
                <th>胚布编号</th> \
                <th>预排机台</th> \
                <th>是否预排</th> \
                <th>选择</th> \
                <th class="hidden">工卡ID</th> \
                <th class="hidden">机台ID</th> \
            </tr>'
    for i in returnValue[0]:
        returnHTML += ' \
        <tr> \
            <td>%s</td> \
            <td>%s</td> \
            <td>%s</td> \
            <td>%s</td> \
            <td>%s</td> \
            <td><input type="checkbox"></td> \
            <td class="hidden">%s</td> \
            <td class="hidden">%s</td> \
        </tr>' % (i['sOrderNo'], i['sCardNo'], i['sMaterialNo'], i['sEquipmentNo'], i['sCheckType'], i['ID'], i['nHDRID'])
    returnHTML += '</tbody>'
    return returnHTML


# 染色看板-所有数据
@KanBan.route('/PlanDye/AllData')
def PlanDyeAllData():
    return render_template('KanBan_PlanDye/PlanDye_All.html')


# AJAX 得到点击的机台的信息
@KanBan.route('/PlanDye/AJAX/AllData/<equipmentNo>')
def AllData(equipmentNo):
    ID = equipmentNo.split('_')[1]
    returnData = IDGetAllData(ID)
    returnEquipment = IDGetEquipment(ID)
    returnHTML = ''

    for i in returnEquipment:
        returnHTML += ' <ul class="slot-list" id="Eq_%s"> \
                            <div> \
                                <input class="title_var" type="text" readOnly="true" value=%s> \
                                <span class="input-group-addon title_span_var" style="background-color:#FFFF00; width:1250px; font-size: 12px;" id="basic-addon1">%s</span> \
                                <span class="input-group-addon title_span_var" style="background-color:#FFFF00; width:1250px; font-size: 12px;" id="basic-addon1">预: %s 卡</span> \
                                <span class="input-group-addon title_span_var" style="background-color:#FFFF00; width:1250px; font-size: 12px;" id="basic-addon1">未: %s 卡</span> \
                            </div>' % (i['ID'], i['sEquipmentNo'], i['sEquipmentName'], i['nCheckCount'], i['nNoCheckCount'])

    for i in returnData:
        if str(i['sType']).find('洗缸') != -1:
            returnHTML += '\
                <li class="slot-it em XG_li" id="Card_%s"> \
                    <div class="clearfix XG_div"> \
                        <div> \
                            <div> \
                                <span>%s</span> \
                            </div> \
                            <div> \
                                <span></span> \
                            </div> \
                        </div> \
                    </div> \
                </li>' % (i['ID'], i['sType'])
        else:
            returnHTML += ' \
                            <li class="slot-item li_style" id="Card_%s" style="background-color: %s"> \
                                <div class="float_left border_div" style="background-color: %s;"></div> \
                                <div class="left_div float_left border_right"> \
                                    <ul> \
                                        <li class="border_bottom left_span_li"><span>%s</span></li> \
                                        <li class="border_bottom left_span_li" style="background-color: %s"><span>%s</span></li> \
                                        <li class="border_bottom left_span_li"><span>%s</span></li> \
                                        <li class="border_bottom left_span_li"><span>%s</span></li> \
                                        <li class="border_bottom left_work_li"><span>%s --&gt; %s --&gt; %s</span></li> \
                                    </ul> \
                                </div> \
                                <div class="right_div float_left border_right"> \
                                    <ul> \
                                        <li class="border_bottom right_span_li"><span>%s</span></li> \
                                        <li class="border_bottom right_span_li"><span>投胚:%s</span></li> \
                                        <li class="border_bottom right_span_li"><span>超时:%s</span></li> \
                                        <li class="border_bottom color_li"><span>%s</span></li> \
                                        <li class="border_bottom right_work_li"><span>%s</span></li> \
                                    </ul> \
                                </div> \
                                <div class="float_left border_div" style="background-color: %s;"></div> \
                            </li> \
                        ' % (i['ID'], i['sIsStart'], i['sWorkCode'], i['sOrderNo'], i['sCheckColor'], i['sCardNo'], i['sMaterialNo'], i['sColorNo'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['sSalesName'], i['nFactInputQty'], i['sOverTime'], i['sColorName'], i['tPlanTime'], i['sColorCode'])
    returnHTML += '</ul>'

    print(returnHTML)
    return returnHTML
