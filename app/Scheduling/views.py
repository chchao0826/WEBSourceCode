# -*-coding:utf-8-*-
from . import Scheduling
from flask import render_template, Flask, request, jsonify
from app.views.Scheduling import GetSchedulingData, GetSchedulingDtlData, SchedulingDataZL_PMC, SchedulingSQL_ZL_PMCHDR, SearchOtherCard, Color, SearChEquipment
from app.models.Scheduling import GetEquipment, GetDtlData, GetDtlData, IsHaveCard, UpdateDtl, InsertDtl, IsHaveCard_PMC, InsertDtl_PMC, UpdateDtl_PMC, UpdateLabel_PMC_True, UpdateLabel_PMC_False, DeleteData, getMaxNumber
import time
import os
from app.PyScript.PMC_ZL_Export import CreateExcel

# 整理预排主页
@Scheduling.route('/ZL/')
def index():
    ReturnData_NET = GetSchedulingData('NET')
    ReturnData_BW = GetSchedulingData('BW')
    ReturnData_Other = GetSchedulingData('Others')
    ReturnEquipment = GetEquipment('整理')
    ReturnDtlData = GetSchedulingDtlData()
    return render_template('Scheduling/Scheduling_ZL.html', ReturnData_NET=ReturnData_NET, ReturnData_BW=ReturnData_BW, ReturnData_Other=ReturnData_Other, ReturnEquipment=ReturnEquipment, ReturnDtlData=ReturnDtlData)

# 整理预排更新数据
@Scheduling.route('/ZL/AJAX/Update/<sEquipmentNo>', methods=['GET', 'POST'])
def AJAXEquipment(sEquipmentNo):
    data = request.get_json()
    datetimeVar = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for i in data:
        sCardNo = str(i['sCardNo'])
        nHDRID = str(i['sEquipmentID'])
        nRowNumber = str(i['nRowNumber'])
        uppTrackJobGUID = str(i['uppTrackJobGUID'])
        #  查找卡号是否存在Dtl表中,若存在更新机台号和顺序,不存在进行INSERT
        # print(IsHaveCard(sCardNo))
        VarData = {
            'sCardNo': sCardNo,
            'nHDRID': nHDRID,
            'nRowNumber': nRowNumber,
            'tTime': datetimeVar,
            'uppTrackJobGUID': uppTrackJobGUID,
        }
        print('-----------------------')
        print(VarData)
        print(IsHaveCard(uppTrackJobGUID))
        if IsHaveCard(uppTrackJobGUID):
            print('UPDATE')
            UpdateDtl(VarData)
            # print('----------------')
        else:
            print('INSERT')
            InsertDtl(VarData)
            # print('++++++++++++++++')

    return '123'

# 整理预排刷新数据
@Scheduling.route('/ZL/AJAX/page', methods=['GET', 'POST'])
def AJAXPage():
    DtlData = GetSchedulingDtlData()
    HdrData = GetEquipment('整理')
    AJAXHTML = ''
    for i in HdrData:
        AJAXHTML += ' \
        <div class="section_var"> \
        <ul id=" Ul_%s " class="" name="Ul_%s"> \
            <div class=""> \
                <input class="title_var" type="text" readOnly="true" \
                    name="%s" id="%s" value=%s> \
            </div> \
            <div class="float-left" style="width: 100%%;>' % (i['ID'], i['ID'], i['sEquipmentNo'], i['sEquipmentNo'], i['sEquipmentNo'])

        for a in DtlData:
            if a['nHDRID'] == i['ID']:
                AJAXHTML += '\
                <li class="slot-item" \
                    style="border-left:15px solid %s; border-right:15px solid %s;"> \
                    <div class="clearfix"> \
                        <div class="hover" style=" width:100%% ; "> \
                            <tr class="tr_var"> \
                                <td class=""> \
                                    <input class="input_var" type="text" readOnly="true" \
                                        name="%s" id="%s" \
                                        value="%s"> \
                                    <input type="text" hidden \
                                        name="%s" id="%s" \
                                        value="%s"> \
                                    <div style="z-index:10" class="ex"> \
                                        <tr> \
                                            <td>%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">实际投胚:%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">温度:%s</td><br> \
                                            <td class="td_var">速度:%s</td><br> \
                                            <td class="td_var">耗时:%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                        </tr> \
                                    </div> \
                                </td> \
                            </tr> \
                        </div> \
                    </div> \
                </li>' % (a['sBorderColor'], a['sColorBorder'], a['sCardNo'], a['sCardNo'], a['sCardNo'], a['uppTrackJobGUID'], a['uppTrackJobGUID'], a['uppTrackJobGUID'], a['sCardNo'], a['sMaterialNo'], a['sMaterialLot'], a['sColorNo'], a['nFactInPutQty'], a['sCustomerName'], a['sSalesGroupName'], a['nTemp'], a['nSpeed'], a['nTime'], a['sProductWidth'], a['sProductGMWT'], a['sWorkingProcedureName'])
        AJAXHTML += '\
                </div> \
            </ul> \
        </div>'
    return AJAXHTML

# ---------------------
# 生管预排
@Scheduling.route('/PMC/<sWorkingProcedureName>')
def PMCIndex(sWorkingProcedureName):
    sWorkingProcedureName1 = sWorkingProcedureName
    if sWorkingProcedureName.find('水洗') != -1:
        sWorkingProcedureName1 = '水洗'

    sWorkingProcedureName2 = ''
    if sWorkingProcedureName1 == '水洗' or sWorkingProcedureName == '预定':
        sWorkingProcedureName2 = '预定'
    SchedulingZL_PMCData = SchedulingDataZL_PMC(
        sWorkingProcedureName1, sWorkingProcedureName2)
    SchedulingZL_PMCDataHDR = SchedulingSQL_ZL_PMCHDR(sWorkingProcedureName)
    print(SchedulingZL_PMCData)
    print(SchedulingZL_PMCDataHDR)
    # print('--------' * 12)
    # print(SchedulingZL_PMCDataHDR)
    return render_template('Scheduling/Scheduling_PMC_DX.html', SchedulingZL_PMCData=SchedulingZL_PMCData, SchedulingZL_PMCDataHDR=SchedulingZL_PMCDataHDR)

# 拖拉 AJAX
@Scheduling.route('/PMC/ZL/AJAX/Move', methods=['GET', 'POST'])
def PMCAjaxZL():
    # print('+++++++++++++++++++++++++++++++++')
    data = request.get_json()
    print(data)
    datetimeVar = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for i in data:
        uppTrackJobGUID = str(i['uppTrackJobGUID'])
        nRowNumber = str(i['nRowNumber'])
        sType = str(i['sType'])
        iFlag = IsHaveCard_PMC(uppTrackJobGUID)
        dDict = {
            'uppTrackJobGUID': uppTrackJobGUID,
            'nRowNumber': nRowNumber,
            'sType': sType,
            'tUpdateTime': datetimeVar,
            'sLabel': ''
        }
        if iFlag == False:
            InsertDtl_PMC(dDict)
        else:
            # print(dDict)
            UpdateDtl_PMC(dDict)
    return ''

# AJAX 标记
@Scheduling.route('/PMC/ZL/AJAX/Label/True', methods=['GET', 'POST'])
def PMCAjaxLabelTrue():
    data = request.get_json()
    for i in data:
        uppTrackJobGUID = str(i['uppTrackJobGUID'])
        UpdateLabel_PMC_True(uppTrackJobGUID)
    return ''

# AJAX 标记
@Scheduling.route('/PMC/ZL/AJAX/Label/False', methods=['GET', 'POST'])
def PMCAjaxLabelFalse():
    data = request.get_json()
    for i in data:
        uppTrackJobGUID = str(i['uppTrackJobGUID'])
        UpdateLabel_PMC_False(uppTrackJobGUID)
    return ''

# DeleteData
@Scheduling.route('/PMC/ZL/AJAX/delete', methods=['GET', 'POST'])
def PMCAjaxDeleteData():
    data = request.get_json()
    print(data)
    for i in data:
        uppTrackJobGUID = str(i['uppTrackJobGUID'])
        print(uppTrackJobGUID)
        DeleteData(uppTrackJobGUID)
    return 'Delete OK'

# 下部数据网上移
@Scheduling.route('/PMC/ZL/AJAX/DataUpdate/<sWorkingProcedureName>', methods=['GET', 'POST'])
def PMCAjaxDataUpdate(sWorkingProcedureName):
    data = request.get_json()
    print(data)
    print('-------------')
    nRowNumber = getMaxNumber(sWorkingProcedureName)
    datetimeVar = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for i in data:
        nRowNumber += 1
        VarDict = {
            'sType': i['sType'],
            'uppTrackJobGUID': i['uppTrackJobGUID'],
            'nRowNumber': nRowNumber,
            'tUpdateTime': datetimeVar,
            'sLabel': ''
        }
        print(i)
        uppTrackJobGUID = i['uppTrackJobGUID']
        iFlag = IsHaveCard_PMC(uppTrackJobGUID)
        if iFlag == False:
            InsertDtl_PMC(VarDict)
    return ''

# 更新页面
@Scheduling.route('/PMC/ZL/AJAX/UpdatePage/<sWorkingProcedureName>', methods=['GET', 'POST'])
def PMCAjaxUpdatePage(sWorkingProcedureName):
    sWorkingProcedureName1 = sWorkingProcedureName
    if sWorkingProcedureName.find('水洗') != -1:
        sWorkingProcedureName1 = '水洗'

    sWorkingProcedureName2 = ''
    if sWorkingProcedureName1 == '水洗' or sWorkingProcedureName == '预定':
        sWorkingProcedureName2 = '预定'
    SchedulingSQL_ZL_PMCData = SchedulingDataZL_PMC(
        sWorkingProcedureName1, sWorkingProcedureName2)
    SchedulingSQL_ZL_PMCTop = SchedulingSQL_ZL_PMCHDR(sWorkingProcedureName)
    returnHtml = ''
    returnHtml = '<div class="top-div" id="top-div" style="overflow-y:scroll; height: 40%;"> \
                    <ul id="ul_var" class="" style="margin: 0;padding: 0;">'

    for i in SchedulingSQL_ZL_PMCTop:
        returnHtml += '<li class="slot-item height40 marginLeft40" style="padding: 0; background-color: %s"> \
                            <div class="clearfix height40"> \
                                <div class="hover_PMC" style="width:100%%;"> \
                                    <table class="table"> \
                                        <tr> \
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
                                            <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 生管交期 --> \
                                            <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 耗时 --> \
                                            <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 营业课别 --> \
                                            <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 工卡备注 --> \
                                            <td hidden>%s</td> \
                                            <td style="width: 8%%; line-height: 25px;" class="border-left"></td> \
                                        </tr> \
                                    </table> \
                                </div> \
                            </div> \
                        </li>' % (i['sLabel'], i['nOverTime'], i['sCustomerName'], i['sLocation'], i['sMaterialNo'], i['sMaterialLot'], i['sCardNo'], i['sColorNo'], i['nFactInputQty'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['dReplyDate'], i['dDeliveryDate'], i['nPSTime'], i['sSalesGroupName'], i['sRemark'],  i['uppTrackJobGUID'])

    returnHtml += '\
            </ul> \
                </div> \
                <div style="margin-left:-40px;"> \
                    <ul> \
                        <li> \
                            <div class=""> \
                                <div class="hover_PMC" style="width:100%;"> \
                                    <table class="table" style="background-color:#EEE0E5;"> \
                                        <tr style="text-align: center;"> \
                                            <td style="width: 4%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 10%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 8%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 3%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 8%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 9%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left" id="count_tr"></td> \
                                            <td style="width: 5%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left" id="sum_time"></td> \
                                            <td style="width: 8%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 10%; line-height: 10px; font-size: 0.8em; font-weight: 700" class="border-left"></td> \
                                            <td style="width: 8%; line-height: 25px;" class="border-left"></td> \
                                        </tr> \
                                    </table> \
                                </div> \
                            </div> \
                        </li> \
                    </ul> \
                </div> \
                <div style="background-color:#000; height:5px;"></div> \
                <div class="bottom-div" id="bottom-div" style="overflow-y:scroll;" style="position: fixed; height: 45%;"> \
                        <ul id="" class="" style="margin: 0;padding: 0;"> '

    for i in SchedulingSQL_ZL_PMCData:
        returnHtml += '<li class="slot-item height40 marginLeft40" style="padding: 0;"> \
                            <div class="clearfix height40"> \
                                <div class="hover_PMC" style="width:100%%; background-color: %s;"> \
                                    <table class="table"> \
                                        <tr> \
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
                                            <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 生管交期 --> \
                                            <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 耗时 --> \
                                            <td style="width: 8%%; line-height: 25px;" class="border-left">%s</td> <!-- 营业课别 --> \
                                            <td style="width: 10%%; line-height: 25px;" class="border-left">%s</td> <!-- 工卡备注 --> \
                                            <td hidden>%s</td> \
                                            <td style="width: 8%%; line-height: 25px;" class="border-left"></td> \
                                        </tr> \
                                    </table> \
                                </div> \
                            </div> \
                        </li>' % (i['sLabel'], i['nOverTime'], i['sCustomerName'], i['sLocation'], i['sMaterialNo'], i['sMaterialLot'], i['sCardNo'], i['sColorNo'], i['nFactInputQty'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['dReplyDate'], i['dDeliveryDate'], i['nPSTime'], i['sSalesGroupName'], i['sRemark'],  i['uppTrackJobGUID'])

    returnHtml += '</div> \
                </ul> \
            </div> \
        </div> \
        <script> \
            getScreen(); \
            getCount(); \
        </script>'

    return returnHtml

# 生管整理看板搜索功能
@Scheduling.route('/PMC/ZL/AJAX/Search/<InputVar>', methods=['GET', 'POST'])
def PMCAjaxSearchCard(InputVar):
    # print(InputVar)
    inputList = InputVar.split('_')
    sWorkingProcedureName = inputList[1]
    if sWorkingProcedureName.find('水洗') != -1:
        sWorkingProcedureName = '预定'
    SearchData = SearchOtherCard(inputList[0], sWorkingProcedureName)
    # print(SearchData)
    # returnHtml = ''
    returnHtml = '<ul id="" class="" style="margin: 0;padding: 0;">'
    for i in SearchData:
        # print()
        returnHtml += ' \
            <li class = "slot-item height40 marginLeft40" style = "padding: 0;" > \
                <div class="clearfix height40"> \
                    <div class="hover_PMC" style="width:100%%;"> \
                        <table class="table"> \
                            <tr> \
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
                                <td style="width: 5%%; line-height: 25px;" class="border-left">%s</td> <!-- 业务交期 --> \
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

# 备注
@Scheduling.route('/PMC/ZL/Remark')
def PMCZLRemark():
    return render_template('Scheduling/Remark.html')

# 生管预排定型打印
@Scheduling.route('/PMC/ZL/Print/<sWorkingProcedureName>')
def PMCZLPrint(sWorkingProcedureName):
    SchedulingSQL_ZL_PMC = SchedulingSQL_ZL_PMCHDR(sWorkingProcedureName)
    print('----------------------')
    print(SchedulingSQL_ZL_PMC)
    return render_template('Scheduling/print_PMC_DX.html', SchedulingSQL_ZL_PMC = SchedulingSQL_ZL_PMC)

# 导出数据EXCEL
@Scheduling.route('/PMC/ZL/ExportExecl')
def PMCZLExportExecl():
    CreateExcel()

# 生管染色预排
@Scheduling.route('/PMC/Dyeing')
def PMCDyeing():
    EquipmentList = SearChEquipment('A群组(HISAK机)')
    return render_template('Scheduling/Scheduling_PMC_Dyeing.html', EquipmentList=EquipmentList)


# 颜色
@Scheduling.route('/Color/')
def ColorCode():
    returnColor = Color()
    return render_template('Scheduling/Color.html', returnColor=returnColor)


