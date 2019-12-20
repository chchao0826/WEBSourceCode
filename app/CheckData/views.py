# -*- coding: utf-8 -*-
from . import CheckData
from flask import Flask, render_template, jsonify, request
from app.CheckData.SQLExec.checkData import JSSearchData
import json


# 研发数据对比_主页
@CheckData.route('/JS/')
def JSCheckData():
    return render_template('checkData/JS.html')


#研发数据对比_AJAX
@CheckData.route('/JS/AJAX/<CardList>')
def jSAJAX(CardList):
    sList1 = ''.join(CardList).split('_')
    sWorkingProcedureName = sList1[0]
    sMaterialNoList = sList1[1].split(',')
    ToList = []
    for i in sMaterialNoList:
        ToList.append(i)
    print(ToList)
    print('=======12312')
    print(sWorkingProcedureName)
    GetData = JSSearchData(sWorkingProcedureName, ToList)
    print(GetData)
    returnHtml = ''   
    returnHtml += ' <tbody> \
                        <tr>'
    if sWorkingProcedureName == 'title':
        returnHtml += ' <tbody> \
                    <tr>'
        returnHtml += '<td>卡号</td>'
        nNumber = 0
        for i in GetData:
            if nNumber == 0:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr id="sMaterialNo"> \
                                <td>布种/LOT</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])              
            elif nNumber == 1:
                returnHtml += ' <td id="1" onclick="SignMain(\'1\')" >%s</td> \
                                <td id="2" onclick="SignMain(\'2\')" >%s</td> \
                                <td id="3" onclick="SignMain(\'3\')" >%s</td> \
                                <td id="4" onclick="SignMain(\'4\')" >%s</td> \
                                <td id="5" onclick="SignMain(\'5\')" >%s</td> \
                                <td id="6" onclick="SignMain(\'6\')" >%s</td> \
                                <td id="7" onclick="SignMain(\'7\')" >%s</td> \
                                <td id="8" onclick="SignMain(\'8\')" >%s</td> \
                                <td id="9" onclick="SignMain(\'9\')" >%s</td> \
                            </tr> \
                            <tr> \
                                <td>来源名称</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 2:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>规格</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 3:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                        </tbody>'%(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            nNumber += 1     
    elif sWorkingProcedureName == 'PR':
        returnHtml += ' <tbody> \
            <tr>'
        returnHtml += '<td>幅宽 cm</td>'
        nNumber = 0
        for i in GetData:
            if nNumber == 1:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>码重 g/y</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])              
            elif nNumber == 2:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>纬密 CPI</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 3:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>克重 g/m²</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 4:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                        </tbody>'%(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            nNumber += 1   
    elif sWorkingProcedureName == 'FS':
        returnHtml += ' <tbody> \
            <tr>'
        returnHtml += '<td>幅宽 cm</td>'
        nNumber = 0
        for i in GetData:
            if nNumber == 1:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>码重 g/y</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])              
            elif nNumber == 2:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>纬密 CPI</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 3:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>克重 g/m²</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 4:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                        </tbody>'%(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            nNumber += 1  
    elif sWorkingProcedureName == 'SC':
        returnHtml += ' <tbody> \
            <tr>'
        returnHtml += '<td>机号</td>'
        nNumber = 0
        for i in GetData:
            if nNumber == 1:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>速度</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])              
            elif nNumber == 2:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>张力</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 3:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>温度</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 4:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>幅宽 cm</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 5:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>码重 g/y</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])                                
            elif nNumber == 5:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>纬密CPI</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])     
            elif nNumber == 6:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>克重 g/m²</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])     
            elif nNumber == 7:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                        </tbody>'%(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            nNumber += 1  
    elif sWorkingProcedureName == 'PS':
        returnHtml += ' <tbody> \
            <tr>'
        returnHtml += '<td>机号</td>'
        nNumber = 0
        for i in GetData:
            if nNumber == 1:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>车速</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])              
            elif nNumber == 2:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>温度设定</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 3:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>幅宽设定 cm</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 4:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>幅宽 cm</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 5:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>码重 g/y</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])                                
            elif nNumber == 5:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>纬密CPC</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])     
            elif nNumber == 6:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>克重 g/m²</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])     
            elif nNumber == 7:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                        </tbody>'%(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            nNumber += 1  
    elif sWorkingProcedureName == 'DY':
        returnHtml += ' <tbody> \
            <tr>'
        returnHtml += '<td>机号</td>'
        nNumber = 0
        for i in GetData:
            if nNumber == 1:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>保温时间</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])              
            elif nNumber == 2:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>染色温度</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 3:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>染色助剂</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 4:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>幅宽 cm</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 5:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>码重 g/y</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])                                
            elif nNumber == 6:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>纬密CPC</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])     
            elif nNumber == 7:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>克重 g/m²</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])     
            elif nNumber == 8:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                        </tbody>'%(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            nNumber += 1  
    elif sWorkingProcedureName == 'SE':
        returnHtml += ' <tbody> \
            <tr>'
        returnHtml += '<td>机号</td>'
        nNumber = 0
        for i in GetData:
            if nNumber == 1:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>车速 m/min</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])              
            elif nNumber == 2:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>温度设定</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 3:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>成定助剂</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 4:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>幅宽设定 cm</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            elif nNumber == 5:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>幅宽 cm</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])                                
            elif nNumber == 6:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>码重 g/y</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])     
            elif nNumber == 7:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>纬密 CPC</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])     
            elif nNumber == 8:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                            <tr> \
                                <td>克重 g/m²</td>' %(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])                                     
            elif nNumber == 9:
                returnHtml += ' <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                                <td>%s</td> \
                            </tr> \
                        </tbody>'%(i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8])
            nNumber += 1  



    return returnHtml




