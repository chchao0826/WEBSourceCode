# -*-coding:utf-8-*-

from . import PlanDye
from flask import render_template, Flask, request, jsonify, json
from app.PlanDye.SQLExec.Dyeing import DyeingData, DyeingEquipment, IDGetData, IDGetEquipment, searchValue
from app.PlanDye.Models.PlanDyeing import UpdateDtl_PMC, UpdateXG_PMC, DeleteXG_PMC, IsHaveXG
from app.PlanDye.SQLExec.DyeingExport import DyeingData
import time
import os


# 主页
@PlanDye.route('/')
def index():
    # sEquipmentModelName = ''
    # getData = DyeingData(sEquipmentModelName)
    # getEquipmentData = DyeingEquipment(sEquipmentModelName)
    # print(getData)
    # print(getEquipmentData)
    # , EquipmentData = getEquipmentData, Cardlist = getData
    return render_template('PlanDye/PMC_Dye.html')


# AJAX 点击机台组别更新机台号
@PlanDye.route('/AJAX/equipment/<equipmentNo>', methods=['GET', 'POST'])
def AjaxData(equipmentNo):
    print(equipmentNo)
    getEuqList = DyeingEquipment(equipmentNo)
    returnHTML = ''
    nLength = str(round(99 / len(getEuqList), 2)) + '%'
    for i in getEuqList:
        returnHTML += '<li id="equ_%s" style="width: %s"><a onclick="btnEqui(\'equ_%s\')">%s</a></li>' % (
            i['ID'], nLength, i['ID'], i['sEquipmentNo'])

    return returnHTML


# AJAX 得到点击的机台的信息
@PlanDye.route('/AJAX/Data/<equipmentNo>')
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


# 保存按钮
@PlanDye.route('/AJAXPOST', methods=['GET', 'POST'])
def AJAXPost():
    data_byte = request.get_data()
    data_str = data_byte.decode()
    data_dict = json.loads(data_str)
    iFlag = False
    a = 0
    sXGList = []
    sEqui = []
    for i in data_dict:
        if i['sCardNo'] != '洗缸':
            UpdateDtl_PMC(i)
        else:
            UpdateXG_PMC(i)
            print(i)
            sDict = {
                'nHDRID': i['nHDRID'],
                'sType': i['sCardNo']
            }
            if sDict not in sXGList:
                sXGList.append(sDict)
        if i['nHDRID'] not in sEqui:
            sEqui.append(i['nHDRID'])
    for i in sEqui:
        # 所有有的数据
        iFlag = False
        returnData = IsHaveXG(i)
        print('------------=============------------121')
        print(returnData)
        print(sXGList)
        for i in returnData:
            if i not in sXGList:
                print('==================')
                print(i)
                DeleteXG_PMC(i)

            print(i)
    return '123'


# 化验室区分
@PlanDye.route('/HYS')
def HYS():
    return render_template('PlanDye/PMC_Dye_HYS.html')


# 搜索更新标题栏
@PlanDye.route('/Search/<inputValue>')
def Search(inputValue):
    retundata = searchValue(inputValue)
    returnHTML = ''
    print(retundata)
    for i in retundata:
        print(i)
        returnHTML += '<span id="span_%s" style="color:#F00;" > %s / %s / %s / %s &nbsp|||</span>' % (
            i['nHDRID'], i['sCardNo'], i['sEquipmentNo'], i['sMaterialNo'], i['sWorkingProcedureNameCurrent'])
    return returnHTML


# 搜索更新机台列表
@PlanDye.route('/SearchUpdateEqui/<inputValue>')
def SearchUpdateEuqi(inputValue):

    sGetEqui = searchValue(inputValue)[0]
    print('==============212121121212===========')
    print(sGetEqui)
    sVar = 'a' + '_' + str(sGetEqui['nHDRID'])
    returnHTML = Equipment(sVar)

    return returnHTML


# 右侧机台更新
@PlanDye.route('SearchUpdateRightEqui/<inputValue>')
def SearchUpdateRightEqui(inputValue):
    sInputvalue = inputValue.split('_')[0]
    sHasEqui = ''.join(inputValue.split('_')[1])
    sHasEquiList = sHasEqui.split(',')
    sGetEqui = searchValue(sInputvalue)[0]
    sEquipmentList = []
    returnHTML = ''
    a = 0
    for c in sHasEquiList:
        sEquiList = IDGetEquipment(c)
        if sEquiList != []:
            for i in sEquiList:
                sDict = {
                    'nHDRID': i['ID'],
                    'sEquipmentNo': i['sEquipmentNo'],
                }
            if sDict not in sEquipmentList:
                sEquipmentList.append(sDict)
                a += 1
    sDict = {
        'nHDRID': sGetEqui['nHDRID'],
        'sEquipmentNo': sGetEqui['sEquipmentNo'],
    }
    if sDict not in sEquipmentList:
        sEquipmentList.append(sDict)
        a += 1
    nWidth = str(round((100 / a), 2))
    for i in sEquipmentList:
        print(nWidth)
        returnHTML += "<li style=\"width: %s%%;\" id=\"addEuqi_equ_%s\"><a onclick=\"clearEqui('addEuqi_equ_%s')\">%s</a></li>" % (
            nWidth, i['nHDRID'], i['nHDRID'], i['sEquipmentNo'])
    return returnHTML


# 导出表格
@PlanDye.route('AJAXExport')
def AJAXExport():
    returnData = DyeingData()
    print(returnData)
    returnHTML = '<table class="table"> \
                    <tr> \
                        <th>sEquipmentNo</th> \
                        <th>sPlanEquipmentNo</th> \
                        <th>sOverTime</th> \
                        <th>sCustomerName</th> \
                        <th>sCardNo</th> \
                        <th>sMaterialNo</th> \
                        <th>sMaterialLot</th> \
                        <th>sColorNo</th> \
                        <th>nFactInputQty</th> \
                        <th>sWorkingProcedureNameLast</th> \
                        <th>sWorkingProcedureNameCurrent</th> \
                        <th>sWorkingProcedureNameNext</th> \
                        <th>nDyeingTime</th> \
                        <th>sLocation</th> \
                        <th>sRemark</th> \
                        <th>sOrderNo</th> \
                    </tr>'
    a = 0
    for i in returnData:
        returnHTML += ' \
                <tr> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                    <td>%s</td> \
                </tr>' % (i['sEquipmentNo'], i['sPlanEquipmentNo'], i['sOverTime'], i['sCustomerName'], i['sCardNo'], i['sMaterialNo'], i['sMaterialLot'], i['sColorNo'], i['nFactInputQty'], i['sWorkingProcedureNameLast'], i['sWorkingProcedureNameCurrent'], i['sWorkingProcedureNameNext'], i['nDyeingTime'], i['sLocation'], i['sRemark'], i['sOrderNo'])
        a += 1
    returnHTML += '</table>'
    print(a)
    return returnHTML


# # 根据机台号AJAX数据
# @PlanDye.route('/AJAX/<sEquipmentModelName>')
# def AJAXEquipment(sEquipmentModelName):
#     getData = DyeingData(sEquipmentModelName)
#     getEquipmentData = DyeingEquipment(sEquipmentModelName)
#     returnHtml = ''
#     for Eq in getEquipmentData:
#         returnHtml += ' <div class="section"> \
#                             <ul id="%s" class="slot-list"> \
#                                 <div class=""> \
#                                     <input class="title_var" type="text" readOnly="true" name="sCardNo%s" id="sCardNo%s"  value = %s> \
#                                         <span class="input-group-addon title_span_var" \
#                                             style="background-color:#FFFF00; width:140px; font-size: 12px;" id="basic-addon1">%s</span> \
#                                         </div>'%(Eq['ID'], Eq['ID'], Eq['ID'], Eq['sEquipmentNo'], Eq['sEquipmentName'])


#         for sVar in getData:
#             if sVar['sEquipmentNo'] == Eq['sEquipmentNo']:
#                 returnHtml += ' <li class="slot-item li_style" id="%s" style="border-left:10px solid %s; border-right:10px solid %s; "> \
#                                     <div class="clearfix"> \
#                                         <div class="float_left left_div border_right"> \
#                                             <div type="text" class="left_1 hover border_bottom"> \
#                                                 <span>%s</span> \
#                                             </div> \
#                                             <div class="left_2 border_bottom"> \
#                                                 <span>%s --> %s</span> \
#                                             </div> \
#                                             <div class="left_3"> \
#                                                 <span>%s</span> \
#                                             </div> \
#                                         </div> \
#                                         <div class="float_left right_div"> \
#                                             <div class="right_1 border_bottom border_right float_left right_1_left" style="background-color: %s; "> \
#                                                 <span>预</span> \
#                                             </div> \
#                                             <div class="right_1 border_bottom border_right float_left right_1_mid" style="background-color: %s; "> \
#                                                 <span>化</span> \
#                                             </div> \
#                                             <div class="right_1 border_bottom border_right float_left right_1_right" style="background-color: %s; "> \
#                                                 <span>染%s</span> \
#                                             </div> \
#                                             <div class="right_2 border_bottom"> \
#                                                 <span>投胚: %s</span> \
#                                             </div> \
#                                             <div class="right_3 border_bottom"> \
#                                                 <span>滞留: %s</span> \
#                                             </div> \
#                                             <div class="right_4 border_bottom"> \
#                                                 <span>%s</span> \
#                                             </div> \
#                                         </div> \
#                                     </div> \
#                                 </li>'%(sVar['ID'], sVar['sWorkCode'], sVar['sColorCode'], sVar['sCardNo'], sVar['sWorkingProcedureNameLast'], sVar['sWorkingProcedureNameCurrent'], sVar['sCustomerName'], sVar['sPSColor'], sVar['sIsHYS'], sVar['sDyeingColor'], sVar['sDyeingCount'], sVar['nFactInputQty'], sVar['sOverTime'], sVar['sMaterialNo'])

#         returnHtml += '</ul> \
#                 </div>'

#     return returnHtml


# {% for Eq in EquipmentData%}
#                 <div class="section">
#                     <ul id="{{Eq.ID}}" class="slot-list">
#                         <div class="">
#                             <input class="title_var" type="text" readOnly="true" name="sCardNo{{Eq.ID}}"
#                                 id="sCardNo{{Eq.ID}}" value={{Eq.sEquipmentNo}}>
#                             <span class="input-group-addon title_span_var"
#                                 style="background-color:#FFFF00; width:140px; font-size: 12px;"
#                                 id="basic-addon1">{{Eq.sEquipmentName}}</span>
#                         </div>
#                         {% for sVar in Cardlist %}
#                         {% if sVar.sEquipmentNo == Eq.sEquipmentNo %}
#                         <li class="slot-item li_style" id="{{sVar.id}}"
#                             style="border-left:10px solid {{sVar.sWorkCode}}; border-right:10px solid {{sVar.sColor16}}; ">
#                             <div class="clearfix">
#                                 <div class="float_left left_div border_right">
#                                     <div type="text" class="left_1 hover border_bottom">
#                                         <span>{{sVar.sCardNo}}</span>
#                                     </div>
#                                     <div class="left_2 border_bottom">
#                                         <span>{{sVar.sWorkingProcedureNameLast}} -->
#                                             {{sVar.sWorkingProcedureNameCurrent}}</span>
#                                     </div>
#                                     <div class="left_3">
#                                         <span>{{sVar.sCustomerName}}</span>
#                                     </div>
#                                 </div>
#                                 <div class="float_left right_div">
#                                     <div class="right_1 border_bottom border_right float_left right_1_left"
#                                         style="background-color: {{sVar.sPSColor}}; ">
#                                         <span>预</span>
#                                     </div>
#                                     <div class="right_1 border_bottom border_right float_left right_1_mid"
#                                         style="background-color: {{sVar.sIsHYS}}; ">
#                                         <span>化</span>
#                                     </div>
#                                     <div class="right_1 border_bottom border_right float_left right_1_right"
#                                         style="background-color: {{sVar.sDyeingColor}}; ">
#                                         <span>染{{sVar.sDyeingCount}}</span>
#                                     </div>
#                                     <div class="right_2 border_bottom">
#                                         <span>投胚: {{sVar.nFactInputQty}} </span>
#                                     </div>
#                                     <div class="right_3 border_bottom">
#                                         <span>滞留: {{sVar.sOverTime}} </span>
#                                     </div>
#                                     <div class="right_4 border_bottom">
#                                         <span>{{sVar.sMaterialNo}} </span>
#                                     </div>
#                                     <div></div>
#                                     <div></div>
#                                 </div>
#                             </div>

#                         </li>
#                         {% endif %}
#                         {% endfor %}
#                     </ul>
#                 </div>
#                 {% endfor %}


# # 机台分组列表显示
# @app.route('/<sEquipmentPrepareNo_var>/',methods=['GET', 'POST'])
# def sCardNo_Walkthrough(sEquipmentPrepareNo_var):
#     if request.method == 'POST':
#         data = request.get_data()
#         data = data.decode()
#         # 更新数据
#         update_rownumber(data)

#         # 获取当前地址
#         path_var = request.path
#         # path_var = path_var.decode()
#         path_var = path_var.split('/')[1:]
#         path_var = ''.join(path_var)
#         path_var = path_var.split('/')[:1]


#     # print(search_list(sEquipmentPrepareNo_var)[0])
#     return render_template('sCardNo_Walkthrough.html',sEquipmentPrepareNo_list_wait = wait_list()[2], sCardNo_list_wait = wait_list()[1], sCardNo_list = search_list(sEquipmentPrepareNo_var)[0],sEquipmentPrepareNo_list = search_list(sEquipmentPrepareNo_var)[1])

# # 机台详细列表
# @app.route('/Detail/<sEquipmentPrepareNo_var>',methods=['GET', 'POST'])
# def sCardNo_Detail(sEquipmentPrepareNo_var):
#     if request.method == 'POST':
#         data = request.get_data()
#         data = data.decode()
#         update_rownumber(data)

#     return render_template('sCardNo_Detail.html',sEquipmentPrepareNo_list_wait = wait_list()[2], sCardNo_list_wait = wait_list()[1], sCardNo_list = search_list(sEquipmentPrepareNo_var)[0],sEquipmentPrepareNo_list = search_list(sEquipmentPrepareNo_var)[1])

# # 236 数据同步
# @app.route('/DataTo236',methods=['GET', 'POST'])
# def DataTo_236():
#     DataTo236_var = DataTo236()
#     expect_list_var = expect_list()
#     wait_list_var = wait_list()
#     return render_template('index.html',sEquipmentPrepareNo_list = expect_list_var[2],sCardNo_list = expect_list_var[1], sEquipmentPrepareNo_list_wait = wait_list_var[2], sCardNo_list_wait = wait_list_var[0])

# # 253 数据同步
# @app.route('/DataToFact',methods=['GET', 'POST'])
# def DataTo_Fact():
#     DataToFact_var = DataToFact()
#     expect_list_var = expect_list()
#     wait_list_var = wait_list()
#     return render_template('index.html',sEquipmentPrepareNo_list = expect_list_var[2],sCardNo_list = expect_list_var[1], sEquipmentPrepareNo_list_wait = wait_list_var[2], sCardNo_list_wait = wait_list_var[0])

# # 保留前五其他顺序更新
# @app.route('/UpdateTop10',methods=['GET', 'POST'])
# def UpdateOther_RowNumber():
#     updateOtherRowNumber()
#     expect_list_var = expect_list()
#     wait_list_var = wait_list()
#     return render_template('index.html',sEquipmentPrepareNo_list = expect_list_var[2],sCardNo_list = expect_list_var[1], sEquipmentPrepareNo_list_wait = wait_list_var[2], sCardNo_list_wait = wait_list_var[0])

# # 所有顺序更新
# @app.route('/UpdateAll',methods=['GET', 'POST'])
# def UpdateAll_RowNumber():
#     updateALLRowNumber()
#     expect_list_var = expect_list()
#     wait_list_var = wait_list()
#     return render_template('index.html',sEquipmentPrepareNo_list = expect_list_var[2],sCardNo_list = expect_list_var[1], sEquipmentPrepareNo_list_wait = wait_list_var[2], sCardNo_list_wait = wait_list_var[0])

# # 预定数据
# @app.route('/PSExpect/',methods=['GET', 'POST'])
# def PSExpect():
#     if request.method == 'POST':
#         data = request.get_data()
#         data = data.decode()
#         print(data)
#         # print(12112121)
#         PSUpdate(data)
#     return render_template('PSExpect.html',PSWaitExpect = PSExpectEP(sEquipmentPrepareNo = '待排'), PSExpectEm1 = PSExpectEP(sEquipmentPrepareNo = '1#'), PSExpectEm2 = PSExpectEP(sEquipmentPrepareNo = '2#'), PSExpectEm3 = PSExpectEP(sEquipmentPrepareNo = '3#'), PSExpectEm4 = PSExpectEP(sEquipmentPrepareNo = '4#'),PSRemark = PSRemark())

# # 预定数据更新
# @app.route('/PSExpect/UpdateTo236/',methods=['GET', 'POST'])
# def PSExpectUpdate():
#     PSDataUpdate()
#     return render_template('PSExpect.html',PSWaitExpect = PSExpectEP(sEquipmentPrepareNo = '待排'), PSExpectEm1 = PSExpectEP(sEquipmentPrepareNo = '1#'), PSExpectEm2 = PSExpectEP(sEquipmentPrepareNo = '2#'), PSExpectEm3 = PSExpectEP(sEquipmentPrepareNo = '3#'), PSExpectEm4 = PSExpectEP(sEquipmentPrepareNo = '4#'),PSRemark = PSRemark())

# @app.route('/PSExpect/UpdateTo253/',methods=['GET', 'POST'])
# def PSExpectUpdateTo253():
#     PS236To253()
#     return render_template('PSExpect.html',PSWaitExpect = PSExpectEP(sEquipmentPrepareNo = '待排'), PSExpectEm1 = PSExpectEP(sEquipmentPrepareNo = '1#'), PSExpectEm2 = PSExpectEP(sEquipmentPrepareNo = '2#'), PSExpectEm3 = PSExpectEP(sEquipmentPrepareNo = '3#'), PSExpectEm4 = PSExpectEP(sEquipmentPrepareNo = '4#'),PSRemark = PSRemark())

# @app.route('/PSExpect/Remark',methods=['GET', 'POST'])
# def PSExpectRemark():
#     if request.method == 'POST':
#         data = request.values.get("sRemark")
#         PSRemark(data)
#         # print(data)
#     return render_template('PSExpect.html',PSWaitExpect = PSExpectEP(sEquipmentPrepareNo = '待排'), PSExpectEm1 = PSExpectEP(sEquipmentPrepareNo = '1#'), PSExpectEm2 = PSExpectEP(sEquipmentPrepareNo = '2#'), PSExpectEm3 = PSExpectEP(sEquipmentPrepareNo = '3#'), PSExpectEm4 = PSExpectEP(sEquipmentPrepareNo = '4#'),PSRemark = PSRemark())
