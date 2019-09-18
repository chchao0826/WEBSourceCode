# -*-coding:utf-8-*-
from . import plan
from flask import render_template, Flask, request, jsonify
from app.views.plan import GetWorking, Data_NoPlan, Data_Plan, SearchAllData, SearchEquipment, Data_DXNoPlan, Data_DXPlan
# from app.models.plan import GetEquipment, GetDtlData, GetDtlData, IsHaveCard, UpdateDtl, InsertDtl, IsHaveCard_PMC, InsertDtl_PMC, UpdateDtl_PMC, UpdateLabel_PMC_True, UpdateLabel_PMC_False, DeleteData, getMaxNumber, OperationalData, DeleteDtl
from app.models.plan import PMCPostData, GetEquipment, DXPostdata, DeleteDXPlan
import time
import os
# from app.PyScript.PMC_ZL_Export import CreateExcel


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
    print(sWoring)
    nCount = ''
    if sWoring in ('SXJ1', 'SXJ2'):
        nRow = sWoring.find('1')
        if nRow == -1:
            nRow = sWoring.find('2')
        sWoring = sWoring[:nRow]
        nCount = sWoring[nRow:]
    sWoring = GetWorking(sWoring)[0]

    print(sWoring + nCount)
    NoPlanData = Data_NoPlan(sWoring + nCount)
    returnData = SearchAllData(sValue, sWoring)
    print(returnData)
    # returnHtml = ''
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
    print(data)
    PMCPostData(data)
    return '生管数据更新'


# PMC操作说明
@plan.route('/PMC/Operation')
def PMC_Operation():
    return render_template('plan/PMC_Operation.html')


# 定型
# 定型预排
@plan.route('/DX/<sWorkingProcedureName>')
def DXIndex(sWorkingProcedureName):
    sEquipmentID = ''
    sWorkingName = GetWorking(sWorkingProcedureName)[0]

    ReturnData = Data_DXNoPlan(sWorkingName)
    ReturnEquipment = GetEquipment('整理')
    ReturnDtlData = Data_DXPlan(sEquipmentID)
    # print(ReturnData)
    # print(ReturnEquipment)
    # print(ReturnDtlData)

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
    print('aaaaaaaaaaaaaaaaaaaaaaaaaa')
    print(sWorkingProcedureName)
    ReturnData = Data_DXNoPlan(sWorkingProcedureName)
    print(ReturnData)
    print('ggggggggggggggggggggggggg')
    LeftPage = '<tbody>'
    print(ReturnData)
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


# # 拖拉 AJAX
# @plan.route('/PMC/ZL/AJAX/Move', methods=['GET', 'POST'])
# def PMCAjaxZL():
#     # print('+++++++++++++++++++++++++++++++++')
#     data = request.get_json()
#     # print(data)
#     datetimeVar = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     for i in data:
#         uppTrackJobGUID = str(i['uppTrackJobGUID'])
#         nRowNumber = str(i['nRowNumber'])
#         sType = str(i['sType'])
#         iFlag = IsHaveCard_PMC(uppTrackJobGUID)
#         dDict = {
#             'uppTrackJobGUID': uppTrackJobGUID,
#             'nRowNumber': nRowNumber,
#             'sType': sType,
#             'tUpdateTime': datetimeVar,
#             'sLabel': ''
#         }
#         if iFlag == False:
#             InsertDtl_PMC(dDict)
#         else:
#             # print(dDict)
#             UpdateDtl_PMC(dDict)
#     return ''

# # AJAX 标记
# @plan.route('/PMC/ZL/AJAX/Label/True', methods=['GET', 'POST'])
# def PMCAjaxLabelTrue():
#     data = request.get_json()
#     for i in data:
#         uppTrackJobGUID = str(i['uppTrackJobGUID'])
#         UpdateLabel_PMC_True(uppTrackJobGUID)
#     return ''

# # AJAX 标记
# @plan.route('/PMC/ZL/AJAX/Label/False', methods=['GET', 'POST'])
# def PMCAjaxLabelFalse():
#     data = request.get_json()
#     for i in data:
#         uppTrackJobGUID = str(i['uppTrackJobGUID'])
#         UpdateLabel_PMC_False(uppTrackJobGUID)
#     return ''

# # DeleteData
# @plan.route('/PMC/ZL/AJAX/delete', methods=['GET', 'POST'])
# def PMCAjaxDeleteData():
#     data = request.get_json()
#     # print(data)
#     for i in data:
#         uppTrackJobGUID = str(i['uppTrackJobGUID'])
#         # print(uppTrackJobGUID)
#         DeleteData(uppTrackJobGUID)
#     return 'Delete OK'

# # 下部数据网上移
# @plan.route('/PMC/ZL/AJAX/DataUpdate/<sWorkingProcedureName>', methods=['GET', 'POST'])
# def PMCAjaxDataUpdate(sWorkingProcedureName):
#     if sWorkingProcedureName == 'PS':
#         sWorkingProcedureName = '预定'
#     elif sWorkingProcedureName == 'SH':
#         sWorkingProcedureName = '成定'
#     elif sWorkingProcedureName == 'SX1':
#         sWorkingProcedureName = '水洗'
#     elif sWorkingProcedureName == 'SX2':
#         sWorkingProcedureName = '水洗'
#     data = request.get_json()
#     # print(data)
#     # print('-------------')
#     nRowNumber = getMaxNumber(sWorkingProcedureName)
#     datetimeVar = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
#     for i in data:
#         nRowNumber += 1
#         VarDict = {
#             'sType': i['sType'],
#             'uppTrackJobGUID': i['uppTrackJobGUID'],
#             'nRowNumber': nRowNumber,
#             'tUpdateTime': datetimeVar,
#             'sLabel': ''
#         }
#         # print(i)
#         uppTrackJobGUID = i['uppTrackJobGUID']
#         iFlag = IsHaveCard_PMC(uppTrackJobGUID)
#         if iFlag == False:
#             InsertDtl_PMC(VarDict)
#     return ''

# # 更新页面
# @plan.route('/PMC/ZL/AJAX/UpdatePage/<sWorkingProcedureName>', methods=['GET', 'POST'])
# def PMCAjaxUpdatePage(sWorkingProcedureName):
#     if sWorkingProcedureName == 'PS':
#         sWorkingProcedureName = '预定'
#     elif sWorkingProcedureName == 'SH':
#         sWorkingProcedureName = '成定'
#     elif sWorkingProcedureName == 'SX1':
#         sWorkingProcedureName = '水洗'
#     elif sWorkingProcedureName == 'SX2':
#         sWorkingProcedureName = '水洗'
#     planSQL_ZL_PMCData = planDataZL_PMC(
#         sWorkingProcedureName, sWorkingProcedureName)
#     planSQL_ZL_PMCTop = planSQL_ZL_PMCHDR(sWorkingProcedureName)
#     returnHtml = ''
#     returnHtml = '<div class="top-div" id="top-div" style="overflow-y:scroll; height: 40%;"> \
#                     <ul id="ul_var" class="" style="margin: 0;padding: 0;">'

#     for i in planSQL_ZL_PMCTop:
#         returnHtml += '<li class="slot-item height40 marginLeft40" style="padding: 0; background-color: %s"> \
#                             <div class="clearfix height40"> \
#                                 <div class="hover_PMC" style="width:100%%;"> \
#                                     <table class="table"> \
#                                         <tr> \
#                                             <td style="width: 4%%; line-height: 25px;" class="border-left">%s</td> <!-- 超时 --> \
#                                             <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 客户名称 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 布车号 --> \
#                                             <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 物料编号 --> \
#                                             <td style="width: 3%%; line-height: 25px;" class="border-left">%s</td> <!-- LOT --> \
#                                             <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 卡号 --> \
#                                             <td style="width: 9%%; line-height: 25px;" class="border-left">%s</td> <!-- 色号 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 投胚 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 上工段 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 现工段 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 下工段 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 生管交期 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 生管交期 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 耗时 --> \
#                                             <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 营业课别 --> \
#                                             <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 工卡备注 --> \
#                                             <td hidden>%s</td> \
#                                             <td style="width: 8%%; line-height: 25px;" class="border-left"></td> \
#                                         </tr> \
#                                     </table> \
#                                 </div> \
#                             </div> \
#                         </li>' % (i['sLabel'], i['nOverTime'], i['sCustomerName'], i['sLocation'], i['sMaterialNo'], i['sMaterialLot'], i['sCardNo'], i['sColorNo'], i['nFactInputQty'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['dReplyDate'], i['dDeliveryDate'], i['nPSTime'], i['sSalesGroupName'], i['sRemark'],  i['uppTrackJobGUID'])

#     returnHtml += '\
#             </ul> \
#                 </div> \
#                 <div style="margin-left:-40px;"> \
#                     <ul> \
#                         <li> \
#                             <div class=""> \
#                                 <div class="hover_PMC" style="width:100%;"> \
#                                     <table class="table" style="background-color:#EEE0E5;"> \
#                                         <tr style="text-align: center;"> \
#                                             <td style="width: 4%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 10%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 8%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 3%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 8%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 9%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left" id="count_tr"></td> \
#                                             <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left" id="sum_time"></td> \
#                                             <td style="width: 8%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 10%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
#                                             <td style="width: 8%; line-height: 25px;" class="border-left"></td> \
#                                         </tr> \
#                                     </table> \
#                                 </div> \
#                             </div> \
#                         </li> \
#                     </ul> \
#                 </div> \
#                 <div style="background-color:#000; height:5px;"></div> \
#                 <div class="bottom-div" id="bottom-div" style="overflow-y:scroll;" style="position: fixed; height: 45%;"> \
#                         <ul id="" class="" style="margin: 0;padding: 0;"> '

#     for i in planSQL_ZL_PMCData:
#         returnHtml += '<li class="slot-item height40 marginLeft40" style="padding: 0;"> \
#                             <div class="clearfix height40"> \
#                                 <div class="hover_PMC" style="width:100%%; background-color: %s;"> \
#                                     <table class="table"> \
#                                         <tr> \
#                                             <td style="width: 4%%; line-height: 25px;" class="border-left">%s</td> <!-- 超时 --> \
#                                             <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 客户名称 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 布车号 --> \
#                                             <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 物料编号 --> \
#                                             <td style="width: 3%%; line-height: 25px;" class="border-left">%s</td> <!-- LOT --> \
#                                             <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 卡号 --> \
#                                             <td style="width: 9%%; line-height: 25px;" class="border-left">%s</td> <!-- 色号 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 投胚 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 上工段 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 现工段 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 下工段 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 生管交期 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 生管交期 --> \
#                                             <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 耗时 --> \
#                                             <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 营业课别 --> \
#                                             <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 工卡备注 --> \
#                                             <td hidden>%s</td> \
#                                             <td style="width: 8%%; line-height: 25px;" class="border-left"></td> \
#                                         </tr> \
#                                     </table> \
#                                 </div> \
#                             </div> \
#                         </li>' % (i['sLabel'], i['nOverTime'], i['sCustomerName'], i['sLocation'], i['sMaterialNo'], i['sMaterialLot'], i['sCardNo'], i['sColorNo'], i['nFactInputQty'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['dReplyDate'], i['dDeliveryDate'], i['nPSTime'], i['sSalesGroupName'], i['sRemark'],  i['uppTrackJobGUID'])

#     returnHtml += '</div> \
#                 </ul> \
#             </div> \
#         </div> \
#         <script> \
#             getScreen(); \
#             getCount(); \
#         </script>'

#     return returnHtml

# # 生管整理看板搜索功能
# @plan.route('/PMC/ZL/AJAX/Search/<InputVar>', methods=['GET', 'POST'])
# def PMCAjaxSearchCard(InputVar):
#     # print(InputVar)
#     inputList = InputVar.split('_')
#     sWorkingProcedureName = inputList[1]
#     if sWorkingProcedureName.find('水洗') != -1:
#         sWorkingProcedureName = '预定'
#     SearchData = SearchOtherCard(inputList[0], sWorkingProcedureName)
#     # print(SearchData)
#     # returnHtml = ''
#     returnHtml = '<ul id="" class="" style="margin: 0;padding: 0;">'
#     for i in SearchData:
#         # print()
#         returnHtml += ' \
#             <li class = "slot-item height40 marginLeft40" style = "padding: 0;" > \
#                 <div class="clearfix height40"> \
#                     <div class="hover_PMC" style="width:100%%;"> \
#                         <table class="table"> \
#                             <tr> \
#                                 <td style="width: 4%%; line-height: 25px;" class="border-left">%s</td> <!-- 超时 --> \
#                                 <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 客户名称 --> \
#                                 <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 布车号 --> \
#                                 <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 物料编号 --> \
#                                 <td style="width: 3%%; line-height: 25px;" class="border-left">%s</td> <!-- LOT --> \
#                                 <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 卡号 --> \
#                                 <td style="width: 9%%; line-height: 25px;" class="border-left">%s</td> <!-- 色号 --> \
#                                 <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 投胚 --> \
#                                 <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 上工段 --> \
#                                 <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 现工段 --> \
#                                 <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 下工段 --> \
#                                 <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 生管交期 --> \
#                                 <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 业务交期 --> \
#                                 <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 耗时 --> \
#                                 <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 营业课别 --> \
#                                 <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 工卡备注 --> \
#                                 <td hidden>%s</td> \
#                             </tr> \
#                         </table> \
#                     </div> \
#                 </div> \
#             </li> \
#         ' % (i['nOverTime'], i['sCustomerName'], i['sLocation'], i['sMaterialNo'], i['sMaterialLot'], i['sCardNo'], i['sColorNo'], i['nFactInputQty'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['dReplyDate'], i['dDeliveryDate'], i['nPSTime'], i['sSalesGroupName'], i['sRemark'],  i['uppTrackJobGUID'])

#     returnHtml += '</ul>'

#     return returnHtml

# # 备注
# @plan.route('/PMC/ZL/Remark')
# def PMCZLRemark():
#     return render_template('plan/Remark.html')

# # 定型数据更新
# @plan.route('/PMC/ZL/Updata/', methods=['GET', 'POST'])
# def PMCZLUpdata():
#     # ReturnData = ExecUpdata()
#     # print(ReturnData)
#     print('--------------')
#     # return ReturnData

# # 生管预排定型打印
# @plan.route('/PMC/ZL/Print/<sWorkingProcedureName>')
# def PMCZLPrint(sWorkingProcedureName):
#     if sWorkingProcedureName == 'PS':
#         sWorkingProcedureName = '预定'
#     elif sWorkingProcedureName == 'SH':
#         sWorkingProcedureName = '成定'
#     elif sWorkingProcedureName == 'SX':
#         sWorkingProcedureName = '水洗'
#     planSQL_ZL_PMC = planSQL_ZL_PMCHDR(sWorkingProcedureName)
#     # print('----------------------')
#     # print(planSQL_ZL_PMC)
#     return render_template('plan/print_PMC_DX.html', planSQL_ZL_PMC=planSQL_ZL_PMC)

# # 导出数据EXCEL
# @plan.route('/PMC/ZL/ExportExecl')
# def PMCZLExportExecl():
#     CreateExcel()

# # 生管染色预排
# @plan.route('/PMC/Dyeing')
# def PMCDyeing():
#     EquipmentList = SearChEquipment('A群组(HISAK机)')
#     return render_template('plan/plan_PMC_Dyeing.html', EquipmentList=EquipmentList)


# # 颜色
# @plan.route('/Color/')
# def ColorCode():
#     returnColor = Color()
#     return render_template('plan/Color.html', returnColor=returnColor)


# # 整理预排主页
# @plan.route('/ZL/<sWorkingProcedureName>')
# def DXindex(sWorkingProcedureName):
#     if sWorkingProcedureName == 'PS':
#         sWorkingProcedureName = '预定'
#     elif sWorkingProcedureName == 'SH':
#         sWorkingProcedureName = '成定'
#     sEquipmentID = ''
#     ReturnData = GetplanData(sWorkingProcedureName)
#     ReturnEquipment = GetEquipment('整理')
#     ReturnDtlData = GetplanDtlData(sEquipmentID)
#     return render_template('plan/plan_ZL.html', ReturnData=ReturnData, ReturnEquipment=ReturnEquipment, ReturnDtlData=ReturnDtlData)


# @plan.route('/ZL/AJAXDtl/<sEquipmentID>')
# def AJAXDtl(sEquipmentID):
#     data = GetplanDtlData(sEquipmentID)
#     returnHTML = ''
#     print(data)
#     for i in data:
#         returnHTML += ' \
#         <li class="slot-item" style="border: 0px;"> \
#             <div class="clearfix"> \
#                 <div class="div-card float-left"> \
#                     <div class="float-left" style="width: 160px; border-right: 1px solid #111; height: 100%%; text-align: center; line-height: 55px; text-align: center; line-height: 60px; background-color: %s"> \
#                         <span>%s</span> \
#                     </div> \
#                     <div class="float-left" style="width: 123px;"> \
#                         <div style="border-bottom: 1px solid #111; height: 30px; text-align: center; line-height: 30px;"> \
#                             <span>%s</span> \
#                         </div> \
#                         <div style="text-align: center; line-height: 30px;"> \
#                             <span>%s</span> \
#                         </div> \
#                     </div> \
#                     <div hidden>%s</div> \
#                     <div hidden>%s</div> \
#                     <div hidden>%s</div> \
#                     <div hidden>%s</div> \
#                     <div hidden>%s</div> \
#                     <div hidden>%s</div> \
#                     <div hidden>%s</div> \
#                     <div hidden>%s</div> \
#                     <div hidden>%s</div> \
#                     <div hidden>%s</div> \
#                     <div hidden>%s</div> \
#                 </div> \
#                 <div class="float-left" style="width: 21px; height:60px; background-color:%s; text-align:  center;"></div> \
#             </div> \
#         </li> ' % (i['sBorderColor'], i['sCardNo'], i['sMaterialNo'], i['nTime'], i['uppTrackJobGUID'], i['sCardNo'], i['sMaterialNo'], i['sColorNo'], i['sProductWidth'], i['sProductGMWT'], i['nFactInPutQty'], i['nTime'], i['nTemp'], i['nSpeed'], i['sWorkingProcedureNameCurrent'], i['sColorBorder'])
#     return returnHTML


# @plan.route('/ZL/AJAXUpdata', methods=['GET', 'POST'])
# def AJAXUpdate():
#     data = request.get_json()
#     for i in data:
#         UpdateDtl(i)
#     return '123'


# @plan.route('/ZL/AJAXDelete', methods=['GET', 'POST'])
# def AJAXDelete():
#     data = request.get_json()
#     for i in data:
#         print(i)
#         DeleteDtl(i)
#     return '123'


# @plan.route('/ZL/AJAXRightPage/<sEquipmentID>', methods=['GET', 'POST'])
# def AJAXRight(sEquipmentID):
#     RightPage = ''
#     RightData = GetplanDtlData(sEquipmentID)
#     for i in RightData:
#         RightPage += '<li class="slot-item" style="border: 0px;"> \
#                         <div class="clearfix"> \
#                             <div class="div-card float-left"> \
#                                 <div class="float-left" style="width: 160px; border-right: 1px solid #111; height: 100%%; text-align: center; line-height: 55px; text-align: center; line-height: 60px; background-color: %s"> \
#                                     <span>%s</span> \
#                                 </div> \
#                                 <div class="float-left" style="width: 123px;"> \
#                                     <div style="border-bottom: 1px solid #111; height: 30px; text-align: center; line-height: 30px;"> \
#                                         <span>%s</span> \
#                                     </div> \
#                                     <div style="text-align: center; line-height: 30px;"> \
#                                         <span>%s</span> \
#                                     </div> \
#                                 </div> \
#                                 <div hidden>%s</div> \
#                                 <div hidden>%s</div> \
#                                 <div hidden>%s</div> \
#                                 <div hidden>%s</div> \
#                                 <div hidden>%s</div> \
#                                 <div hidden>%s</div> \
#                                 <div hidden>%s</div> \
#                                 <div hidden>%s</div> \
#                                 <div hidden>%s</div> \
#                                 <div hidden>%s</div> \
#                                 <div hidden>%s</div> \
#                             </div> \
#                             <div class="float-left" style="width: 21px; height:60px; background-color:%s; text-align: center;"> \
#                             </div> \
#                         </div> \
#                     </li> \
#                     ' % (i['sBorderColor'], i['sCardNo'], i['sMaterialNo'], i['nTime'], i['uppTrackJobGUID'], i['sCardNo'], i['sMaterialNo'], i['sColorNo'], i['sProductWidth'], i['sProductGMWT'], i['nFactInPutQty'], i['nTime'], i['nTemp'], i['nSpeed'], i['sWorkingProcedureNameCurrent'], i['sColorBorder'])
#     return RightPage


# @plan.route('/ZL/AJAXLeftPage/<sWorkingProcedureName>', methods=['GET', 'POST'])
# def AJAXLeft(sWorkingProcedureName):
#     if sWorkingProcedureName == 'PS':
#         sWorkingProcedureName = '预定'
#     elif sWorkingProcedureName == 'SH':
#         sWorkingProcedureName = '成定'
#     ReturnData = GetplanData(sWorkingProcedureName)
#     LeftPage = '<tbody>'
#     for i in ReturnData:
#         LeftPage += ' \
#         <tr onclick="onclicktr("%s")" id="%s" style="background-color: %s"> \
#             <td style="width: 10%%;">%s</td> \
#             <td style="width: 10%%;">%s</td> \
#             <td style="width: 10%%;">%s</td> \
#             <td style="width: 10%%;">%s</td> \
#             <td style="width: 10%%;">%s</td> \
#             <td style="width: 10%%;">%s</td> \
#             <td style="width: 10%%;">%s</td> \
#             <td style="width: 10%%;">%s</td> \
#             <td style="width: 10%%;">%s</td> \
#             <td style="width: 10%%;">%s</td> \
#             <td hidden>%s</td> \
#         </tr>' % (i['uppTrackJobGUID'], i['uppTrackJobGUID'], i['sBorderColor'], i['sCardNo'], i['sMaterialNo'], i['sColorNo'], i['sProductWidth'], i['sProductGMWT'], i['nFactInPutQty'], i['nTime'], i['nTemp'], i['nSpeed'], i['sWorkingProcedureNameCurrent'], i['uppTrackJobGUID'])

#     LeftPage += '</tbody>'
#     return LeftPage
