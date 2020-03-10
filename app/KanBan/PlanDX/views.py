# -*-coding:utf-8-*-
from app.KanBan import KanBan
from flask import render_template, Flask, request

from app.KanBan.PlanDX.Models.DX import DXKanBanData, DXKanBanChartData
from app.Plan.Models.plan import GetEquipment
from app.KanBan.PlanDX.SQLExec.PlanDX import Data_PlanDX, SearchFun

import json


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


# 定型看板查询
@KanBan.route('/Plan/DX')
def DXKanBan_Plan():
    returnData = Data_PlanDX('LB01')
    return render_template('KanBan/PlanDX.html', returnData=returnData)


# 点击机台操作
@KanBan.route('/Plan/DX/<sEquipmentNo>')
def DXKanBan_Plan_ClickEq(sEquipmentNo):
    returnData = Data_PlanDX(sEquipmentNo)
    returnHtml = '<tbody> \
                    <tr class="ThTr"> \
                        <th>超时</th> \
                        <th>预排机台</th>\
                        <th>预排回数</th>\
                        <th>生管回数</th>\
                        <th>预计完成时间</th>\
                        <th>实际完成时间</th>\
                        <th>生管上传时间</th>\
                        <th>订单号</th>\
                        <th>卡号</th>\
                        <th>客户名称</th>\
                        <th>布车号</th>\
                        <th>物料编号</th>\
                        <th>LOT</th>\
                        <th>色号</th>\
                        <th>投胚</th>\
                        <th>上工段</th>\
                        <th>现工段</th>\
                        <th>下工段</th>\
                        <th>生交期</th>\
                        <th>业交期</th>\
                        <th>耗时</th>\
                        <th>营业课别</th>\
                        <th>工卡备注</th>\
                    </tr>'
    for i in returnData:
        returnHtml += ' \
            <tr class="%s"> \
            <td>%s</td> \
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td name = "sOrderNo">%s</td>\
            <td name = "sCardNo">%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td name = "sMaterialNo">%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
        </tr>' % (i['sLabel'], i['sOverTime'], i['sEquipmentNo'], i['nRowNumber'], i['nPMCNumber'], i['tPlanTime'], i['tFactEndTime'], i['tUpdateTime'], i['sOrderNo'], i['sCardNo'], i['sCustomerName'], i['sLocation'], i['sMaterialNo'], i['sMaterialLot'], i['sColorNo'], i['nFactInputQty'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['dReplyDate'], i['dDeliveryDate'], i['nTime'], i['sSalesGroupName'], i['sRemark'])
    returnHtml += "</tbody>"
    return returnHtml


# 搜索查询数据
@KanBan.route('/Plan/DX/Search/<sSearchValue>')
def DXKanBan_Plan_Search(sSearchValue):
    returnList = SearchFun(sSearchValue)
    returnData = returnList[0]
    print(returnData)
    returnEquipment = returnList[1]
    returnHtml = '\
        <tbody> \
            <tr class="ThTr"> \
                <th>超时</th> \
                <th>预排机台</th>\
                <th>预排回数</th>\
                <th>生管回数</th>\
                <th>预计完成时间</th>\
                <th>实际完成时间</th>\
                <th>生管上传时间</th>\
                <th>订单号</th>\
                <th>卡号</th>\
                <th>客户名称</th>\
                <th>布车号</th>\
                <th>物料编号</th>\
                <th>LOT</th>\
                <th>色号</th>\
                <th>投胚</th>\
                <th>上工段</th>\
                <th>现工段</th>\
                <th>下工段</th>\
                <th>生交期</th>\
                <th>业交期</th>\
                <th>耗时</th>\
                <th>营业课别</th>\
                <th>工卡备注</th>\
            </tr>'
    for i in returnData:
        returnHtml += ' \
            <tr class="%s"> \
            <td>%s</td> \
            <td name="sEquipmentNo">%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td name = "sOrderNo">%s</td>\
            <td name = "sCardNo">%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td name = "sMaterialNo">%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
            <td>%s</td>\
        </tr>' % (i['sLabel'], i['sOverTime'], i['sEquipmentNo'], i['nRowNumber'], i['nPMCNumber'], i['tPlanTime'], i['tFactEndTime'], i['tUpdateTime'], i['sOrderNo'], i['sCardNo'], i['sCustomerName'], i['sLocation'], i['sMaterialNo'], i['sMaterialLot'], i['sColorNo'], i['nFactInputQty'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['dReplyDate'], i['dDeliveryDate'], i['nTime'], i['sSalesGroupName'], i['sRemark'])
    returnHtml += "</tbody>"
    return returnHtml
