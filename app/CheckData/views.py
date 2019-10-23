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

    GetData = JSSearchData(sWorkingProcedureName, ToList)
    returnHtml = ''       
    returnHtml += ' <tbody> \
                        <tr>'
    if sWorkingProcedureName == '主页':
        returnHtml += '<td>卡号</td>'
        for i in GetData:
            returnHtml += '<td>%s</td>' %(i[0])
        returnHtml += '<td>布种/LOT</td>'
        for i in GetData:
            returnHtml += '<td>%s</td>' %(i[1])
        returnHtml += '<td>来源名称</td>'
        for i in GetData:
            returnHtml += '<td>%s</td>' %(i[2])
        returnHtml += '<td>规格</td>'
        for i in GetData:
            returnHtml += '<td>%s</td>' %(i[3])                        

    return returnHtml

    