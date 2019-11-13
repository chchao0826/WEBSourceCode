# -*-coding:utf-8-*-
from . import PlanDye
from flask import render_template, Flask, request, jsonify
from app.PlanDye.SQLExec.Dyeing import DyeingData, DyeingEquipment
from app.PlanDye.Models.PlanDyeing import UpdateDtl_PMC

import time
import os

@PlanDye.route('/<sEquipmentModelName>')
def index(sEquipmentModelName):
    # sEquipmentModelName = ''
    getData = DyeingData(sEquipmentModelName)
    getEquipmentData = DyeingEquipment(sEquipmentModelName)
    print(getData)
    print(getEquipmentData)
    return render_template('PlanDye/PMC_Dye.html', EquipmentData = getEquipmentData, Cardlist = getData)


# AJAX POST DATA 数据更新
@PlanDye.route('/AjaxData', methods=['GET', 'POST'])
def AjaxData():
    data = request.get_json()
    for i in data:
        print(i)
        UpdateDtl_PMC(i)    
    return '后端发现'


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
