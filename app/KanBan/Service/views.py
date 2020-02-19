# -*-coding:utf-8-*-
from app.KanBan import KanBan
from flask import render_template, Flask, request

from app.KanBan.Service.SQLExec.EquipmentService import equipmentServiceData

import json

# 故障检修看板
@KanBan.route('/service')
def equipmentService():
    returnData = equipmentServiceData()
    return render_template('KanBan/equipmentService.html', returnData=returnData[0], nCount=returnData[1], nAllPage=returnData[2])


# 故障看板点击页码
@KanBan.route('/service/page/<nPage>')
def ServiceAJAXPage(nPage):
    returnData = equipmentServiceData(nPage)[0]
    returnHTML = ''
    print(returnData)
    for i in returnData:
        print('================')
        print(i)
        returnHTML += '\
            <div class="col-md-2 col_style"> \
                <ul class="ul_style"> \
                    <li> \
                        <div class="circle" style="background-color: %s;"></div> \
                    </li> \
                    <li class="col_title"> \
                        <span>%s单</span> \
                    </li> \
                    <li> \
                        <div style="border-top: 2px dashed #111;"></div> \
                    </li> \
                    <li> \
                        <span>%s</span> \
                        <span> - </span> \
                        <span>%s</span> \
                    </li> \
                    <li> \
                        <span>%s</span> \
                    <li> \
                        <span>%s</span> \
                        <span> - </span> \
                        <span>%s</span> \
                    <li style="height:70px;"> \
                        <span>%s</span> \
                    </li> \
                    <li> \
                        <div style="border-top: 2px solid #111;"></div> \
                    </li> \
                    <li> \
                        <span>受理人员:</span> \
                        <span>%s</span> \
                    </li> \
                    <li> \
                        <span>目前状态:</span> \
                        <span>%s</span> \
                    </li> \
                    <li> \
                        <span>%s</span> \
                    </li> \
                </ul> \
            </div>' % (i['sStatus'], i['sServiceType'], i['sWorkCentreName'], i['sReportName'], i['sEquipmentNo'], i['sEquipmentDetailType'], i['sEquipmentDetail'], i['sFaultReason'], i['sServiceName'], i['sServiceStatus'], i['sTime'])
    return returnHTML
