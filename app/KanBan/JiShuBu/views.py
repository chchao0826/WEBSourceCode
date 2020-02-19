# -*-coding:utf-8-*-
from app.KanBan import KanBan
from flask import render_template, Flask, request

from app.KanBan.JiShuBu.SQLExec.JSInformation import JSData

import json


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
