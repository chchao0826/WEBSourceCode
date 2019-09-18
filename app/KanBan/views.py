# -*-coding:utf-8-*-
from . import kanban
from flask import render_template, Flask, request
from app.views.kanban import emStatus, StoreStatus, wpStatus, JSData
import json


# 主页
@kanban.route('/')
def index():
    return render_template('kanban/base.html')


# 工厂平面图
@kanban.route('/floorplan/')
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

    return render_template('kanban/floorPlan.html', TJ_eq = TJ_eq, MM_eq = MM_eq, Dye_eq1 = Dye_eq1, Dye_eq2 = Dye_eq2, Dye_eq3 = Dye_eq3, Dye_eq4 = Dye_eq4, Dye_eq5 = Dye_eq5, Dye_eq6 = Dye_eq6, PB_eq = PB_eq, DB_eq = DB_eq, TS_eq = TS_eq, FB_eq = FB_eq, SX_eq = SX_eq, DX_eq1 = DX_eq1, DX_eq2 = DX_eq2, DJ_eq = DJ_eq, YB_eq = YB_eq, TJ_WIP = TJ_WIP, SX_WIP = SX_WIP, YD_WIP = YD_WIP, Dye_WIP = Dye_WIP, DX_WIP = DX_WIP, YB_WIP = YB_WIP, DJ_WIP = DJ_WIP, FP = FP, STA = STA, STC = STC)

 
# 技术部看板
@kanban.route('/JS/')
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
    return render_template('kanban/JSInformation.html', returnData = cardData, salesGroupList = salesGroupList, nPage = nPage)


# AJAX
@kanban.route('/JS/AJAX/sSaleGroupName2/<GetValue>')
def JSDataAJAX(GetValue):
    sSaleGroupName = ''
    nPage = 1
    if GetValue.find('_') == -1:
        sSaleGroupName = GetValue
    else:
        sSaleGroupName = GetValue.split('_')[0]
        nPage = GetValue.split('_')[1]

    returnData = JSData(sSaleGroupName)[0]
    nReturnPage = JSData(sSaleGroupName)[8]
    returnHTML = ''

    for i in returnData:

        if str(nPage) == str(i['nPageNumber']):

            returnHTML +='\
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
                </div>'%(i['borderColor'], i['sMaterialNo'], i['sCardNo'], i['tCardTime'], i['sWorkingProcedureName'], i['sSalesName'], i['sKanBanRemark'])

    returnHTML += '<div class="fixed" id="fixed"> \
                    <nav aria-label="Page navigation"> \
                        <ul class="pagination" style="height:10px; margin-top:-4px;">'
    for i in range(1, nReturnPage + 1):
        # print(i)
        # print(nPage)
        if str(i) == str(nPage):
            returnHTML += '<li class="active"><a href="#" onclick="clickPage(%s)" id="%s" style="font-size: 20px;">%s</a></li>' %(i, i, i)
        else:
            returnHTML += '<li><a href="#" onclick="clickPage(%s)"  id="%s" style="font-size: 20px;">%s</a></li>' %(i, i, i)

    
    returnHTML += '</ul> \
                </nav> \
            </div> \
            <script>PageCenter()</script>'
                    
    print('++++++++++++++++')
    print(returnHTML)
    returnHTML += '<script>scroll();</script>'
    return returnHTML


# AJAX 头部标题
@kanban.route('/JS/AJAXHEADER')
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


# AJAX Title 营业部门 转至 业务员
@kanban.route('/JS/AJAX/sSaleGroupName/<sSaleGroupName>')
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


# AJAX Title 业务员 更新 wrapper
@kanban.route('/JS/AJAX/sSalesName2/<sSaleName>')
def JSDateAJAXSale2(sSaleName):
    returnData = JSData(sSaleName)[4]
    returnHTML = ''
    # print('-----------------')
    for i in returnData:
        returnHTML +='\
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
            </div>'%(i['borderColor'], i['sMaterialNo'], i['sCardNo'], i['tCardTime'], i['sWorkingProcedureName'], i['sSalesName'], i['sKanBanRemark'])
    returnHTML += '<script>scroll();</script>'
    return returnHTML


# AJAX Title 业务员 更新 wrapper + 循环
@kanban.route('/JS/AJAX/sSalesName/<sSaleName>')
def JSDateAJAXSale(sSaleName):
    # print('11111')
    returnData = JSData(sSaleName)[4]
    # print(sSaleName)
    returnHTML = ''
    # print(returnData)
    for i in returnData:
        returnHTML +='\
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


# 技术部工段
@kanban.route('/JS/sWorkingProcedureName/')
def JSPro():
    # print('12222')
    returnData = JSData()
    cardData = []
    for i in returnData[0]:
        if i['nPageNumber'] == 1:
            cardData.append(i)
    workingProcedureList = returnData[9]
    nPage = returnData[8]
    return render_template('kanban/JSWorkingProcedure.html', returnData = cardData, workingProcedureList = workingProcedureList, nPage = nPage)


# # 技术部 工段页面
# @kanban.route('/JS/sWorkingProcedureName/AJAX/<sWorkingProcedureName>')
# def JSProAJAX(sWorkingProcedureName):
#     returnData = JSData(sWorkingProcedureName)[6]
#     returnHTML = ''
#     # print(returnData)
#     for i in returnData:
#         returnHTML +='\
#             <div class="col-md-2" style="height:400px;" onclick="turnOver()"> \
#                 <div class="box direct-chat" style="height:400px; border-top: 6px solid %s"> \
#                     <div class="box-header text-center"> \
#                         <h3 class="box-title" style="font-size: 60px; font-weight: 900;">%s</h3> \
#                     </div> \
#                     <div class="box-body" style="margin-top:-8px; height: 350px;"> \
#                         <div class="direct-chat-messages" style="height: 350px;"> \
#                             <ul class="text-center" style="font-size:50px; font-weight: 500;"> \
#                                 <li>%s</li> \
#                                 <li>%s</li> \
#                                 <li>%s</li> \
#                                 <li>%s</li> \
#                             </ul> \
#                         </div> \
#                         <div class="direct-chat-contacts" style="font-size: 50px; height: 350px;" name="remark"> \
#                             %s \
#                         </div> \
#                     </div> \
#                 </div> \
#             </div>'%(i['borderColor'], i['sMaterialNo'], i['sCardNo'], i['tCardTime'], i['sWorkingProcedureName'], i['sSalesName'], i['sKanBanRemark'])
#     returnHTML += '<script>scroll();</script>'
#     return returnHTML
