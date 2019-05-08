# -*-coding:utf-8-*-
from . import CheckFabric
from flask import render_template, Flask, request, jsonify
from app.views.CheckFabric import GetDetail, GETFabricIn, GetEquipment, GetDefectType, GetDefect, GetUserName, GetViewTitle, GetViewFabric, GetViewOtherDefect, ISHaveuppTrackJobGUID, ISInsertDtl, ISPopupBeginOrSearch, UPDATETable, UPDATETableDefect , SearchCardNo
from app.models.CheckFabric import ses, InspectHdr, InspectDtl, ReturnHdrID, ReturnDtlID, InspectDefect
import json
import time
import eel


@CheckFabric.route('/')
# 主页
def index():
    # returnDetail = GetDetail('\'C190301643\'')
    returnDefectType = GetDefectType()
    returnGetDefect = GetDefect("'22'")
    sUserName = GetUserName()
    return render_template('CheckFabric/CheckFabric.html', returnDefectType=returnDefectType, returnGetDefect=returnGetDefect, sUserName=sUserName)


@CheckFabric.route('/AJAX/Detail/<sCardNo>/')
# AJAX
def AJAXdetail(sCardNo):
    print(sCardNo)
    GetList = sCardNo.split('_')
    CardNo = GetList[0]
    Field = GetList[1]
    print(CardNo)
    print(Field)
    detailList = GetDetail("'" + CardNo + "'")
    if detailList == []:
        detailList = SearchCardNo("'" + CardNo + "'")

    print(detailList)
    readonly = ''
    if Field != 'sLocation':
        readonly = 'readonly'
    for i in detailList:
        sValue = i[Field]
        keyList = i.keys()
        for a in keyList:
            if a == Field:
                returnVar = '<input type="text" class="form-control" %s value=%s>' % (
                    readonly, '"' + sValue + '"')
                print(returnVar)
                return returnVar


@CheckFabric.route('/AJAX/FabricIn/<sCardNo>')
# 根据卡号得到胚布批次
def AJAXFabricIn(sCardNo):
    Fabric = GETFabricIn("'" + sCardNo + "'")
    return render_template('CheckFabric/GetFabric.html', Fabric=Fabric)


@CheckFabric.route('/AJAX/sFabricNo/<sFabricNo>')
# 选择胚布批次后进行赋值
def AJAXFabricNo(sFabricNo):
    GetList = sFabricNo.split('_')
    ID = GetList[0]
    sValue = GetList[1]
    returnHtml = '<input type="text" class="form-control" value = %s>' % (
        sValue)
    return returnHtml


@CheckFabric.route('/AJAX/Group/')
# 班别
def AJAXGroup():
    return render_template('CheckFabric/Group.html')


@CheckFabric.route('/AJAX/Equipment/')
# 机台
def AJAXEquipment():
    sEquipment = GetEquipment()
    return render_template('CheckFabric/Equipment.html', sEquipment=sEquipment)


@CheckFabric.route('/AJAX/Grade/')
# 等级
def AJAXGrade():
    return render_template('CheckFabric/Grade.html')


@CheckFabric.route('/AJAX/defectType/<typeID>/')
# 根据疵点类别获取疵点
def AJAXDefectType(typeID):
    ReturnGetDefect = GetDefect(typeID)
    retrunHtml = '<div class="btn-group" role="group">'
    for i in ReturnGetDefect:
        retrunHtml += '<button type="button" class="btn btn-default btn-defectType" onclick="clickDefect(\'%s\')">%s</button>' % (
            i['sDefectNameCN'], i['sDefectNameCN'])
    retrunHtml += '</div>'
    return retrunHtml


@CheckFabric.route('/AJAX/Defect/')
# 等级
def AJAXPageDefect():
    returnDefectType = GetDefectType()
    returnGetDefect = GetDefect("'22'")
    return render_template('CheckFabric/Defect.html', returnDefectType=returnDefectType, returnGetDefect=returnGetDefect)


@CheckFabric.route('/AJAX/SaveData/HDR/', methods=['GET', 'POST'])
# 主表保存按钮
def AJAXSaveDataHDR():
    data = request.get_json()
    sUserName = ''
    sGroup = ''
    sCardNo = ''
    sEquipment = ''
    uppTrackJobGUID = ''
    usdOrderLotGUID = ''
    ummMaterialGUID = ''
    utmColorGUID = ''
    upsWorkFlowCardGUID = ''

    datetime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for i in data:
        sUserName = str(i['sUserName'])
        sGroup = str(i['sGroup'])
        sCardNo = str(i['sCardNo'])
        sEquipment = str(i['sEquipment'])
        uppTrackJobGUID = i['uppTrackJobGUID']
        usdOrderLotGUID = i['usdOrderLotGUID']
        ummMaterialGUID = i['ummMaterialGUID']
        utmColorGUID = i['utmColorGUID']
        upsWorkFlowCardGUID = i['upsWorkFlowCardGUID']
    iFlag = ISHaveuppTrackJobGUID("'"+uppTrackJobGUID+"'")
    if iFlag == []:
        InspectHdr_var = InspectHdr(sGroupNo=sGroup, sCardNo=sCardNo, sEquipmentName=sEquipment, sCreator=sUserName, tCreateTime=datetime, sUpdateMan=sUserName, tUpdateTime=datetime,
                                    uppTrackJobGUID=uppTrackJobGUID, usdOrderLotGUID=usdOrderLotGUID, ummMaterialGUID=ummMaterialGUID, utmColorGUID=utmColorGUID, upsWorkFlowCardGUID=upsWorkFlowCardGUID)
        ses.add(InspectHdr_var)
        ses.commit()
        ses.close()


@CheckFabric.route('/AJAX/SaveData/DTL/', methods=['GET', 'POST'])
# DTL表保存
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
    uppTrackJobGUID = ''
    for i in data:
        sFabricNo = str(i['sFabricNo']),
        print(i['sFabricNo']),
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
        tInspectTime = i['tTime'],
        uppTrackJobGUID = str(i['uppTrackJobGUID'])
    HdrID = ReturnHdrID(sCardNo)[0]['ID']
    sFabricNo = sFabricNo[0]
    iFlag = ISInsertDtl("'" + uppTrackJobGUID + "'", "'" + sFabricNo + "'")

    if iFlag == []:
        InspectDtl_var = InspectDtl(tInspectTime=tInspectTime, sFabricNo=sFabricNo, nLengthYard=nLengthYard, nWidth=nWidth, sGrade=sGrade, sMainDefectName=sMainDefectName,
                                    nDensity=nDensity, nGMWTLeft=nGMWTLeft, nGMWTInner=nGMWTInner, nGMWTRight=nGMWTRight, sRemark=sRemark, ipbCommonDataHalfInspectHdrID=HdrID)
        ses.add(InspectDtl_var)
        ses.commit()
        ses.close()


@CheckFabric.route('/AJAX/SaveData/Defect/', methods=['GET', 'POST'])
# 疵点表保存
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
        # print(ipbCommonDataHalfInspectDtlID)
        InspectDefect_var = InspectDefect(iNumber=iNo, sDefectTypeName=sDefectName, nScore=nScore,
                                          nSite=nSite, ipbCommonDataHalfInspectDtlID=ipbCommonDataHalfInspectDtlID)
        ses.add(InspectDefect_var)
        ses.commit()
        ses.close()


@CheckFabric.route('/CheckView/<sCardNo>/', methods=['GET', 'POST'])
# 预览界面
def CheckView(sCardNo):
    ViewTitle = GetViewTitle("'" + sCardNo + "'")
    ViewFabric = GetViewFabric("'" + sCardNo + "'")
    ViewOtherDefect = GetViewOtherDefect("'" + sCardNo + "'")
    return render_template('CheckFabric/CheckView.html', ViewTitle=ViewTitle, ViewFabric=ViewFabric, ViewOtherDefect=ViewOtherDefect)


@CheckFabric.route('/popUp/BeginOrSearch/<sCardNo>')
# 判断点击卡号查询后是弹出哪个页面
def popUpBeginOrSearch(sCardNo):
    returnValue = ISPopupBeginOrSearch("'" + sCardNo + "'")[0]
    print(returnValue)
    return jsonify(returnValue)


@CheckFabric.route('/popUp/SearchFlag/<sCardNo>')
# 判断点击卡号查询后是弹出哪个页面
def popUpSearchFlag(sCardNo):
    returnValue = ISPopupBeginOrSearch("'" + sCardNo + "'")[1]
    print(returnValue)
    return jsonify(returnValue)


@CheckFabric.route('/popUp/windows/<sCardNo>')
# 弹窗选择
def popUpWindows(sCardNo):
    returnValue = ISPopupBeginOrSearch("'" + sCardNo + "'")[1]
    print(returnValue)
    return render_template('CheckFabric/popUpSearch.html', returnValue=returnValue)


@CheckFabric.route('/popUp/windows/search/')
# 弹窗查询选择哪一个工段信息
def popUpCheck():
    return render_template('CheckFabric/popUpBeginOrSearch.html')


@CheckFabric.route('/AJAX/TABLE/<VarValue>')
# AJAX INPUT VALUE
def AJAXTable(VarValue):
    GetList = VarValue.split('_')
    Fields = GetList[0]
    ipbCommonDataHalfInspectHdrID = GetList[1]
    ReturnValue = UPDATETable(ipbCommonDataHalfInspectHdrID)[0]
    returnHtml = '<table class="table table-hover" id="CheckData"> \
                <tr> \
                    <th>验布时间</th> \
                    <th>批次</th> \
                    <th>码长</th> \
                    <th>米长</th> \
                    <th>等级</th> \
                    <th>幅宽</th> \
                    <th>主疵点</th> \
                    <th>备注</th>\
                </tr>'
    for i in ReturnValue:
        returnHtml += '<tr id = %s onclick="ClickDTL(%s)"> \
            <td name = %s> %s </td> \
            <td name = %s> %s </td> \
            <td name = %s> %s </td> \
            <td name = %s> %s </td> \
            <td name = %s> %s </td> \
            <td name = %s> %s </td> \
            <td name = %s> %s </td> \
            <td name = %s> %s </td> \
        </tr>'%(i['ID'], i['ID'], 'tInspectTime', i['tInspectTime'], 'sMaterialLot', i['sMaterialLot'], 'nLengthYard', i['nLengthYard'], 'nLengthMeter', i['nLengthMeter'], 'sGrade', i['sGrade'], 'nWidth', i['nWidth'], 'sMainDefectName', i['sMainDefectName'], 'sRemark', i['sRemark'])
    
    returnHtml += '</table>'
    return returnHtml


@CheckFabric.route('/AJAX/INPUT/<VarValue>/')
# AJAX DTLTABLEVALUE
def AJAXInput(VarValue):
    GetList = VarValue.split('_')
    Fields = GetList[0]
    ipbCommonDataHalfInspectHdrID = GetList[1]
    ReturnValue = UPDATETable(ipbCommonDataHalfInspectHdrID)[1]
    readonly = 'readonly'
    for i in ReturnValue:
        sValue = i[Fields]
        keyList = i.keys()
        for a in keyList:
            if a == Fields:
                returnVar = '<input type="text" class="form-control" %s value=%s>' % (
                    readonly, '"' + str(sValue) + '"')
                print(returnVar)
                return returnVar



@CheckFabric.route('/AJAX/TABLEDefect/<ipbCommonDataHalfInspectDtlID>')
# AJAXDefect  UPDATETableDefect
def AJAXTableDefect(ipbCommonDataHalfInspectDtlID):
    print('12121212')
    ReturnValue = UPDATETableDefect(ipbCommonDataHalfInspectDtlID)
    returnHtml = '<table class="table table-hover" id=""defectTable""> \
                <tr> \
                    <th>序号</th> \
                    <th>疵点名称</th> \
                    <th>分数</th> \
                    <th>位置</th> \
                </tr>'
    for i in ReturnValue:
        returnHtml += '<tr id = %s onclick="ClickDTL(%s)"> \
            <td name = %s> %s </td> \
            <td name = %s> %s </td> \
            <td name = %s> %s </td> \
            <td name = %s> %s </td> \
        </tr>'%('ID', i['ID'], 'iNumber', i['iNumber'], 'sDefectTypeName', i['sDefectTypeName'], 'nScore', i['nScore'], 'nSite', i['nSite'])
    
    returnHtml += '</table>'
    return returnHtml


