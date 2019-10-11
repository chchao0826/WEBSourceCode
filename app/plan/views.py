# -*-coding:utf-8-*-
from . import plan
from flask import render_template, Flask, request, jsonify
from app.views.plan import GetWorking, Data_NoPlan, Data_Plan, SearchAllData, SearchEquipment, Data_DXNoPlan, Data_DXPlan, importData_PMC
from app.models.plan import PMCPostData, GetEquipment, DXPostdata, DeleteDXPlan
import time
import os


# --------------------- 生管
# 生管预排
@plan.route('/PMC/<sWorkingProcedureName>')
def PMCIndex(sWorkingProcedureName):
    nCount = ''
    if sWorkingProcedureName in ('SXJ1', 'SXJ2'):
        nRow = sWorkingProcedureName.find('1')
        if nRow == -1:
            nRow = sWorkingProcedureName.find('2')
        nCount = sWorkingProcedureName[nRow:]
        sWorkingProcedureName = sWorkingProcedureName[:nRow]

    sWorkingName = GetWorking(sWorkingProcedureName)[0]
    NoPlanData = Data_NoPlan(sWorkingName)
    PlanData = Data_Plan(sWorkingName + str(nCount))
    return render_template('plan/PMC_DX.html', NoPlanData=NoPlanData, PlanData=PlanData)


# 生管预排搜索数据库中的数据
@plan.route('/PMC/Search/<inputValue>')
def PMCSearch(inputValue):
    sValue = inputValue.split('_')[0]
    sWoring = inputValue.split('_')[1]
    nCount = ''
    if sWoring in ('SXJ1', 'SXJ2'):
        nRow = sWoring.find('1')
        if nRow == -1:
            nRow = sWoring.find('2')
        sWoring = sWoring[:nRow]
        nCount = sWoring[nRow:]
    sWoring = GetWorking(sWoring)[0]

    NoPlanData = Data_NoPlan(sWoring + nCount)
    returnData = SearchAllData(sValue, sWoring)

    returnHtml = '<ul id="bottom_ul" class="" style="margin: 0;padding: 0;">'
    for i in NoPlanData:
        returnHtml += ' \
                    <li class = "slot-item height40 marginLeft40" style = "padding: 0;" > \
                        <div class="clearfix height40"> \
                            <div class="hover_PMC" style="width:100%%;"> \
                                <table class="table"> \
                                    <tr style="text-align: center;"> \
                                        <td style="width: 4%%; line-height: 25px;" class="border-left">%s</td> <!-- 超时 --> \
                                        <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 客户名称 --> \
                                        <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 布车号 --> \
                                        <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 物料编号 --> \
                                        <td style="width: 3%%; line-height: 25px;" class="border-left">%s</td> <!-- LOT --> \
                                        <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 卡号 --> \
                                        <td style="width: 9%%; line-height: 25px;" class="border-left">%s</td> <!-- 色号 --> \
                                        <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 投胚 --> \
                                        <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 上工段 --> \
                                        <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 现工段 --> \
                                        <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 下工段 --> \
                                        <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 生管交期 --> \
                                        <td style="width: 4%%; line-height: 25px;" class="border-left">%s</td> <!-- 业务交期 --> \
                                        <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 耗时 --> \
                                        <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 营业课别 --> \
                                        <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 工卡备注 --> \
                                        <td hidden>%s</td> \
                                    </tr> \
                                </table> \
                            </div> \
                        </div> \
                    </li> \
                ' % (i['nOverTime'], i['sCustomerName'], i['sLocation'], i['sMaterialNo'], i['sMaterialLot'], i['sCardNo'], i['sColorNo'], i['nFactInputQty'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['dReplyDate'], i['dDeliveryDate'], i['nPSTime'], i['sSalesGroupName'], i['sRemark'],  i['uppTrackJobGUID'])
    for i in returnData:
        # print()
        returnHtml += ' \
            <li class = "slot-item height40 marginLeft40 findOut" style = "padding: 0;" > \
                <div class="clearfix height40"> \
                    <div class="hover_PMC" style="width:100%%;"> \
                        <table class="table"> \
                            <tr style="text-align: center;"> \
                                <td style="width: 4%%; line-height: 25px;" class="border-left">%s</td> <!-- 超时 --> \
                                <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 客户名称 --> \
                                <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 布车号 --> \
                                <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 物料编号 --> \
                                <td style="width: 3%%; line-height: 25px;" class="border-left">%s</td> <!-- LOT --> \
                                <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 卡号 --> \
                                <td style="width: 9%%; line-height: 25px;" class="border-left">%s</td> <!-- 色号 --> \
                                <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 投胚 --> \
                                <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 上工段 --> \
                                <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 现工段 --> \
                                <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 下工段 --> \
                                <td style="width: 4%%; line-height: 25px;" class="border-left">%s</td> <!-- 生管交期 --> \
                                <td style="width: 4%%; line-height: 25px;" class="border-left">%s</td> <!-- 业务交期 --> \
                                <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 耗时 --> \
                                <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 营业课别 --> \
                                <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 工卡备注 --> \
                                <td hidden>%s</td> \
                            </tr> \
                        </table> \
                    </div> \
                </div> \
            </li> \
        ' % (i['nOverTime'], i['sCustomerName'], i['sLocation'], i['sMaterialNo'], i['sMaterialLot'], i['sCardNo'], i['sColorNo'], i['nFactInputQty'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['dReplyDate'], i['dDeliveryDate'], i['nPSTime'], i['sSalesGroupName'], i['sRemark'],  i['uppTrackJobGUID'])

    returnHtml += '</ul>'

    return returnHtml


# 生管预排 POST资料
@plan.route('/PMC/PostData', methods=['GET', 'POST'])
def PMC_PostData():
    data = request.get_json()
    PMCPostData(data)
    return '生管数据更新'


# PMC操作说明
@plan.route('/PMC/Operation')
def PMC_Operation():
    return render_template('plan/PMC_Operation.html')


# 导入数据
@plan.route('/PMC/ImportData', methods=['GET', 'POST'])
def PMC_ImportData():
    data = request.get_json()
    importData_PMC(data)
    # print(data)
    return '导入成功'


# 定型
# 定型预排
@plan.route('/DX/<sWorkingProcedureName>')
def DXIndex(sWorkingProcedureName):
    sEquipmentID = ''
    sWorkingName = GetWorking(sWorkingProcedureName)[0]
    ReturnData = Data_DXNoPlan(sWorkingName)
    ReturnEquipment = GetEquipment('整理')
    ReturnDtlData = Data_DXPlan(sEquipmentID)

    return render_template('plan/DX.html', ReturnData=ReturnData, ReturnEquipment=ReturnEquipment, ReturnDtlData=ReturnDtlData)


# 定型AJAX
# 点击机台号进行数据的刷新
@plan.route('/DX/AJAXDtl/<sEquipmentID>')
def checkEquipmentAJAX(sEquipmentID):
    data = Data_DXPlan(sEquipmentID)
    returnHTML = ''
    # print(data)
    for i in data:
        returnHTML += ' \
        <li class="slot-item" style="border: 0px;"> \
            <div class="clearfix"> \
                <div class="div-card float-left"> \
                    <div class="float-left" style="width: 160px; border-right: 1px solid #111; height: 100%%; text-align: center; line-height: 55px; text-align: center; line-height: 60px; background-color: %s"> \
                        <span>%s</span> \
                    </div> \
                    <div class="float-left" style="width: 123px;"> \
                        <div style="border-bottom: 1px solid #111; height: 30px; text-align: center; line-height: 30px;"> \
                            <span>%s</span> \
                        </div> \
                        <div style="text-align: center; line-height: 30px;"> \
                            <span>耗时:</span> \
                            <span>%s</span> \
                        </div> \
                    </div> \
                    <div hidden>%s</div> \
                    <div hidden>%s</div> \
                    <div hidden>%s</div> \
                    <div hidden>%s</div> \
                    <div hidden>%s</div> \
                    <div hidden>%s</div> \
                    <div hidden>%s</div> \
                    <div hidden>%s</div> \
                    <div hidden>%s</div> \
                    <div hidden>%s</div> \
                    <div hidden>%s</div> \
                </div> \
                <div class="float-left" style="width: 21px; height:60px; background-color:%s; text-align:  center;"></div> \
            </div> \
        </li> ' % (i['sBorderColor'], i['sCardNo'], i['sMaterialNo'], i['nTime'], i['uppTrackJobGUID'], i['sCardNo'], i['sMaterialNo'], i['sColorNo'], i['sProductWidth'], i['sProductGMWT'], i['nFactInPutQty'], i['nTime'], i['nTemp'], i['nSpeed'], i['sWorkingProcedureNameCurrent'], i['sColorBorder'])
    return returnHTML


# 更新insert Data
@plan.route('/DX/AJAXInsertData', methods=['GET', 'POST'])
def AJAXInsertData():
    data = request.get_json()
    DXPostdata(data)
    return '定型更新数据成功'


# 删除数据
@plan.route('/DX/AJAXDelete', methods=['GET', 'POST'])
def AJAXDelete():
    data = request.get_json()
    for i in data:
        DeleteDXPlan(i)
    return '123'


# 右边页面刷新
@plan.route('/DX/AJAXRightPage/<sEquipmentID>', methods=['GET', 'POST'])
def AJAXRight(sEquipmentID):
    RightPage = ''
    print(sEquipmentID)
    RightData = Data_DXPlan(sEquipmentID)
    for i in RightData:
        RightPage += '\
            <li class="slot-item" style="border: 0px;"> \
                <div class="clearfix"> \
                    <div class="div-card float-left"> \
                        <div class="float-left" style="width: 160px; border-right: 1px solid #111; height: 100%%; text-align: center; line-height: 55px; text-align: center; line-height: 60px; background-color: %s"> \
                            <span>%s</span> \
                        </div> \
                        <div class="float-left" style="width: 123px;"> \
                            <div style="border-bottom: 1px solid #111; height: 30px; text-align: center; line-height: 30px;"> \
                                <span>%s</span> \
                            </div> \
                            <div style="text-align: center; line-height: 30px;"> \
                                <span>耗时:</span> \
                                <span>%s</span> \
                            </div> \
                        </div> \
                        <div hidden>%s</div> \
                        <div hidden>%s</div> \
                        <div hidden>%s</div> \
                        <div hidden>%s</div> \
                        <div hidden>%s</div> \
                        <div hidden>%s</div> \
                        <div hidden>%s</div> \
                        <div hidden>%s</div> \
                        <div hidden>%s</div> \
                        <div hidden>%s</div> \
                        <div hidden>%s</div> \
                    </div> \
                    <div class="float-left" style="width: 21px; height:60px; background-color:%s; text-align: center;"> \
                    </div> \
                </div> \
            </li> \
            ' % (i['sBorderColor'], i['sCardNo'], i['sMaterialNo'], i['nTime'], i['uppTrackJobGUID'], i['sCardNo'], i['sMaterialNo'], i['sColorNo'], i['sProductWidth'], i['sProductGMWT'], i['nFactInPutQty'], i['nTime'], i['nTemp'], i['nSpeed'], i['sWorkingProcedureNameCurrent'], i['sColorBorder'])
    return RightPage


# 右边页面刷新
@plan.route('/DX/AJAXLeftPage/<sWorkingProcedureName>', methods=['GET', 'POST'])
def AJAXLeft(sWorkingProcedureName):
    if sWorkingProcedureName.find('PS') != -1:
        sWorkingProcedureName = '预定'
    elif sWorkingProcedureName.find('SH') != -1:
        sWorkingProcedureName = '成定'
    sWorkingName = GetWorking(sWorkingProcedureName)[0]
    ReturnData = Data_DXNoPlan(sWorkingName)
    LeftPage = '<tbody>'
    for i in ReturnData:
        LeftPage += ' \
        <tr onclick="onclicktr(\'%s\')" id="%s" style="background-color: %s"> \
            <td style="width: 10%%;">%s</td> \
            <td style="width: 10%%;">%s</td> \
            <td style="width: 10%%;">%s</td> \
            <td style="width: 10%%;">%s</td> \
            <td style="width: 10%%;">%s</td> \
            <td style="width: 10%%;">%s</td> \
            <td style="width: 10%%;">%s</td> \
            <td style="width: 10%%;">%s</td> \
            <td style="width: 10%%;">%s</td> \
            <td style="width: 10%%;">%s</td> \
            <td hidden>%s</td> \
        </tr>' % (i['uppTrackJobGUID'], i['uppTrackJobGUID'], i['sBorderColor'], i['sCardNo'], i['sMaterialNo'], i['sColorNo'], i['sProductWidth'], i['sProductGMWT'], i['nFactInPutQty'], i['nTime'], i['nTemp'], i['nSpeed'], i['sWorkingProcedureName'], i['uppTrackJobGUID'])

    LeftPage += '</tbody>'
    return LeftPage


# 移动后保存按钮
@plan.route('/DX/AJAXSave', methods=['GET', 'POST'])
def AJAXSave():
    data = request.get_json()
    DXPostdata(data)
    return '123'

