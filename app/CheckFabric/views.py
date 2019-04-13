# -*-coding:utf-8-*-
from . import CheckFabric
from flask import render_template, Flask, request
from app.views.CheckFabric import GetDetail, GETFabricIn, GetEquipment, GetDefectType, GetDefect, GetUserName

import json

# 主页
@CheckFabric.route('/')
def index():
    # returnDetail = GetDetail('\'C190301643\'')
    returnDefectType = GetDefectType()
    returnGetDefect = GetDefect("'22'")
    sUserName = GetUserName()
    return render_template('CheckFabric/CheckFabric.html', returnDefectType = returnDefectType, returnGetDefect = returnGetDefect, sUserName = sUserName)

# AJAX
@CheckFabric.route('/AJAX/Detail/<sCardNo>/')
def AJAXdetail(sCardNo):
    GetList = sCardNo.split('_')
    CardNo = GetList[0]
    Field = GetList[1]
    detailList = GetDetail("'"+ CardNo +"'")
    # print(detailList)
    readonly = ''
    if Field != 'sLocation':
        readonly = 'readonly'
    for i in detailList:
        sValue = i[Field]
        keyList = i.keys()
        for a in keyList:
            if a == Field:
                returnVar = '<input type="text" class="form-control" %s value=%s>' %(readonly, '"'+ sValue +'"')
                print(returnVar)
                return returnVar

# 根据卡号得到胚布批次
@CheckFabric.route('/AJAX/FabricIn/<sCardNo>')
def AJAXFabricIn(sCardNo):
    Fabric = GETFabricIn("'"+ sCardNo +"'")
    return render_template('CheckFabric/GetFabric.html', Fabric = Fabric)

# 选择胚布批次后进行赋值
@CheckFabric.route('/AJAX/sFabricNo/<sFabricNo>')
def AJAXFabricNo(sFabricNo):
    GetList = sFabricNo.split('_')
    ID = GetList[0]
    sValue = GetList[1]
    returnHtml ='<input type="text" class="form-control" value = %s>'%(sValue)
    return returnHtml


# 班别
@CheckFabric.route('/AJAX/Group/')
def AJAXGroup():
    return render_template('CheckFabric/Group.html')

# 机台
@CheckFabric.route('/AJAX/Equipment/')
def AJAXEquipment():
    sEquipment = GetEquipment()
    return render_template('CheckFabric/Equipment.html', sEquipment = sEquipment)

# 等级
@CheckFabric.route('/AJAX/Grade/')
def AJAXGrade():
    return render_template('CheckFabric/Grade.html')

# 根据疵点类别获取疵点
@CheckFabric.route('/AJAX/defectType/<typeID>/')
def AJAXDefectType(typeID):
    ReturnGetDefect = GetDefect(typeID)
    retrunHtml = '<div class="btn-group" role="group">'
    for i in ReturnGetDefect:
        retrunHtml += '<button type="button" class="btn btn-default btn-defectType" onclick="clickDefect(\'%s\')">%s</button>' %(i['sDefectNameCN'], i['sDefectNameCN'])
    retrunHtml += '</div>'
    return retrunHtml

# 等级
@CheckFabric.route('/AJAX/Defect/')
def AJAXPageDefect():
    returnDefectType = GetDefectType()
    returnGetDefect = GetDefect("'22'")
    return render_template('CheckFabric/Defect.html', returnDefectType = returnDefectType, returnGetDefect = returnGetDefect)
