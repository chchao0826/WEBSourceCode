# -*-coding:utf-8-*-
from . import Scheduling
from flask import render_template, Flask, request, jsonify
from app.views.Scheduling import GetSchedulingData, GetSchedulingDtlData
from app.models.Scheduling import GetEquipment, GetDtlData, GetDtlData, IsHaveCard, UpdateDtl, InsertDtl
import time

# 主页
@Scheduling.route('/ZL/')
def index():
    ReturnData_NET = GetSchedulingData('NET')
    ReturnData_BW = GetSchedulingData('BW')
    ReturnData_Other = GetSchedulingData('Other')
    ReturnEquipment = GetEquipment('整理')
    ReturnDtlData = GetSchedulingDtlData()
    return render_template('Scheduling/Scheduling_ZL.html', ReturnData_NET=ReturnData_NET, ReturnData_BW=ReturnData_BW, ReturnData_Other=ReturnData_Other, ReturnEquipment=ReturnEquipment, ReturnDtlData=ReturnDtlData)


@Scheduling.route('/ZL/AJAX/Update/<sEquipmentNo>', methods=['GET', 'POST'])
def AJAXEquipment(sEquipmentNo):

    data = request.get_json()
    
    datetimeVar = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(data)
    print(datetimeVar)
    for i in data:
        sCardNo = str(i['sCardNo'])
        nHDRID = str(i['sEquipmentID'])
        nRowNumber = str(i['nRowNumber'])
        #  查找卡号是否存在Dtl表中,若存在更新机台号和顺序,不存在进行INSERT
        # print(IsHaveCard(sCardNo))
        VarData = {
            'sCardNo': sCardNo,
            'nHDRID': nHDRID,
            'nRowNumber': nRowNumber,
            'datetime': datetimeVar,
        }
        if IsHaveCard(sCardNo):
            UpdateDtl(VarData)
            # print('----------------')
        else:
            InsertDtl(VarData)
            # print('++++++++++++++++')

    return '123'


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
            <div class="float-left">' % (i['ID'], i['ID'], i['sEquipmentNo'], i['sEquipmentNo'], i['sEquipmentNo'])

        for a in DtlData:
            if a['nHDRID'] == i['ID']:
                AJAXHTML += '\
                <li class="slot-item" \
                    style="border-left:5px solid %s; border-right:5px solid %s;"> \
                    <div class="clearfix"> \
                        <div class="hover" style=" width:100%% ; "> \
                            <tr class="tr_var"> \
                                <td class=""> \
                                    <input class="input_var" type="text" readOnly="true" \
                                        name="%s" id="%s" \
                                        value="%s"> \
                                    <div style="z-index:10" class="ex"> \
                                        <tr> \
                                            <td>%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td><br> \
                                            <td class="td_var">%s</td> \
                                        </tr> \
                                    </div> \
                                </td> \
                            </tr> \
                        </div> \
                    </div> \
                </li>' % (a['sBorderColor'], a['sColorBorder'], a['sCardNo'], a['sCardNo'], a['sCardNo'], a['sCardNo'], a['sMaterialNo'], a['sMaterialLot'], a['sColorNo'], a['nFactInPutQty'], a['sCustomerName'], a['sSalesGroupName'], a['nPSTime'], a['nSETime'], a['nPSSpeed'], a['nSESpeed'], a['nPS2Temp'], a['nSETemp'])
        AJAXHTML += '\
                </div> \
            </ul> \
        </div>'
    return AJAXHTML
