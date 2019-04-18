# -*-coding:utf-8-*-
from . import CheckFabric
from flask import render_template, Flask, request
from app.views.CheckFabric import GetDetail, GETFabricIn, GetEquipment, GetDefectType, GetDefect, GetUserName
from app.models.CheckFabric import ses, InspectHdr, InspectDtl, ReturnHdrID, ReturnDtlID, InspectDefect
import json
import time

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

# 主表保存按钮
@CheckFabric.route('/AJAX/SaveData/HDR/', methods = ['GET','POST'])
def AJAXSaveDataHDR():
    data = request.get_json()
    sUserName = ''
    sGroup = ''
    sCardNo = ''
    sEquipment = ''
    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for i in data:
        sUserName = str(i['sUserName'])
        sGroup = str(i['sGroup'])
        sCardNo = str(i['sCardNo'])
        sEquipment = str(i['sEquipment'])
    InspectHdr_var = InspectHdr(sGroupNo = sGroup, sCardNo = sCardNo, sEquipmentName = sEquipment, sCreator = sUserName, tCreateTime = datetime, sUpdateMan = sUserName, tUpdateTime = datetime)

    ses.add(InspectHdr_var)
    ses.commit()
    ses.close()

# DTL表保存
@CheckFabric.route('/AJAX/SaveData/DTL/', methods = ['GET','POST'])
def AJAXSaveDataDTL():
    data = request.get_json()
    sFabricNo = ''
    nLengthYard = ''
    nWidth = ''
    sGrade = ''
    sMainDefectName = ''
    nDensity = ''
    nGMWTLeft = ''
    nGMWTInner = ''
    nGMWTRight = ''
    sRemark = ''
    sCardNo = ''
    for i in data:
        sFabricNo = i['sFabricNo'],
        nLengthYard = float(i['nLength']),
        nWidth = float(i['nWidth']),
        sGrade = i['sGrade'],
        sMainDefectName = i['sDefect'],
        nDensity = float(i['nDensity']),
        nGMWTLeft = float(i['nGMWTLeft']),
        nGMWTInner = float(i['nGMWTInner']),
        nGMWTRight = float(i['nGMWTRight']),
        sRemark = i['sRemark'],
        sCardNo = i['sCardNo'],
        tInspectTime = i['tTime']
    HdrID = ReturnHdrID(sCardNo)[0]['ID']
    InspectDtl_var = InspectDtl(tInspectTime = tInspectTime, sFabricNo = sFabricNo, nLengthYard = nLengthYard, nWidth = nWidth, sGrade = sGrade, sMainDefectName = sMainDefectName,nDensity = nDensity, nGMWTLeft = nGMWTLeft, nGMWTInner = nGMWTInner, nGMWTRight = nGMWTRight, sRemark = sRemark, ipbCommonDataHalfInspectHdrID = HdrID)
    ses.add(InspectDtl_var)
    ses.commit()
    ses.close()

# 疵点表保存
@CheckFabric.route('/AJAX/SaveData/Defect/', methods = ['GET','POST'])
def AJAXSaveDataDefect():
    data = request.get_json()
    iNo = ''
    sDefectName = ''
    nScore = ''
    nSite = ''
    tCheckTime = ''
    ipbCommonDataHalfInspectDtlID = ''
    for i in data:
        tCheckTime = i['tCheckTime']
        iNo = i['ID'],
        sDefectName = i['sDefectName'],
        nScore = float(i['nScore']),
        nSite = i['nSite']

        ipbCommonDataHalfInspectDtlID = ReturnDtlID(tCheckTime)[0]['ID']
        print(ipbCommonDataHalfInspectDtlID)
        InspectDefect_var = InspectDefect(iNumber = iNo, sDefectTypeName = sDefectName, nScore = nScore, nSite = nSite, ipbCommonDataHalfInspectDtlID = ipbCommonDataHalfInspectDtlID)
        ses.add(InspectDefect_var)
        ses.commit()
        ses.close()


# 预览界面
@CheckFabric.route('/CheckView/', methods = ['GET','POST'])
def CheckView():
    return render_template('CheckFabric/CheckView.html')
