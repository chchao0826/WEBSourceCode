# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect
from app.sql.plan import SearchEquipmentSQL, GetData_NoPlan, GetData_Plan, GetData_AllNoPlan, SearchWoringSQL, InsertImportData
from app.sql.DXplan import NoDXPlanSQL, DXPlanSQL
from app.models.plan import IsInPMCPlan
import time
# from app.sql.ExecUpdate import ExecUpdateSql

import re


# 236
base = declarative_base()
session = sessionmaker(bind=engine_253)
ses = session()


# 获得当前时间
def GetDate():
    # localtime = time.localtime(time.time())
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


# 工段名称解析
def GetWorking(sWorkingProcedureName):
    ReturnData = []
    sSQL = SearchWoringSQL(sWorkingProcedureName)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        ReturnData.append(row[0])
        row = cursor.fetchone()
    cursor.close()
    return ReturnData


# 生管整理预排SQL
def Data_NoPlan(sWorkingProcedureName):
    ReturnData = []
    print(sWorkingProcedureName)
    sSQL = GetData_NoPlan(sWorkingProcedureName)
    print(sSQL)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'ID': row[0],
            'sIsRush': row[1],
            'sCardNo': row[2],
            'sMaterialNo': row[3],
            'sMaterialLot': row[4],
            'sColorNo': row[5],
            'nFactInputQty': row[6],
            'sWorkingProcedureNameCurrent': row[7],
            'tFactEndTimeLast': row[8],
            'sNotDoneProcedure': row[9],
            'nTJTime': row[10],
            'nPSTime': row[11],
            'nDyeingTime': row[12],
            'nSETime': row[13],
            'sCustomerName': row[14],
            'sSalesName': row[15],
            'sSalesGroupName': row[16],
            'sColorBorder': row[17],
            'nOverTime': row[18],
            'uppTrackJobGUID': row[20],
            'sLocation': row[21],
            'sLabel': row[22],
            'sRemark': row[24],
            'sWorkingProcedureNameLast': row[25],
            'sWorkingProcedureNameNext': row[26],
            'dReplyDate': row[27],
            'dDeliveryDate': row[28],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData


# 生管整理预排主表
def Data_Plan(sWorkingProcedureName):
    ReturnData = []
    sSQL = GetData_Plan(sWorkingProcedureName)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'ID': row[0],
            'sIsRush': row[1],
            'sCardNo': row[2],
            'sMaterialNo': row[3],
            'sMaterialLot': row[4],
            'sColorNo': row[5],
            'nFactInputQty': row[6],
            'sWorkingProcedureNameCurrent': row[7],
            'tFactEndTimeLast': row[8],
            'sNotDoneProcedure': row[9],
            'nTJTime': row[10],
            'nPSTime': row[11],
            'nDyeingTime': row[12],
            'nSETime': row[13],
            'sCustomerName': row[14],
            'sSalesName': row[15],
            'sSalesGroupName': row[16],
            'sColorBorder': row[17],
            'nOverTime': row[18],
            'uppTrackJobGUID': row[20],
            'sLabel': row[21],
            'sLocation': row[22],
            'sRemark': row[23],
            'sWorkingProcedureNameLast': row[24],
            'sWorkingProcedureNameNext': row[25],
            'dReplyDate': row[26],
            'dDeliveryDate': row[27],
            'sType': sWorkingProcedureName,
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    # print(ReturnData)
    if ReturnData == []:
        dictVar = {
            'ID': 1,
            'sIsRush': '',
            'sCardNo': '',
            'sMaterialNo': '',
            'sMaterialLot': '',
            'sColorNo': '',
            'nFactInputQty': '',
            'sWorkingProcedureNameCurrent': '',
            'tFactEndTimeLast': '',
            'sNotDoneProcedure': '',
            'nTJTime': '',
            'nPSTime': '',
            'nDyeingTime': '',
            'nSETime': '',
            'sCustomerName': '',
            'sSalesName': '',
            'sSalesGroupName': '',
            'sColorBorder': '',
            'nOverTime': '',
            'uppTrackJobGUID': '',
            'sLabel': '#FFF',
            'sLocation': '',
            'sRemark': '',
            'sWorkingProcedureNameLast': '',
            'sWorkingProcedureNameNext': '',
            'dReplyDate': '',
            'dDeliveryDate': '',
        }
        ReturnData.append(dictVar)
    cursor.close()
    return ReturnData


# Search其他卡号
def SearchAllData(sFeild, sWoring):
    ReturnData = []
    sSQL = GetData_AllNoPlan(sFeild, sWoring)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'ID': row[0],
            'sIsRush': row[1],
            'sCardNo': row[2],
            'sMaterialNo': row[3],
            'sMaterialLot': row[4],
            'sColorNo': row[5],
            'nFactInputQty': row[6],
            'sWorkingProcedureNameCurrent': row[7],
            'tFactEndTimeLast': row[8],
            'sNotDoneProcedure': row[9],
            'nTJTime': row[10],
            'nPSTime': row[11],
            'nDyeingTime': row[12],
            'nSETime': row[13],
            'sCustomerName': row[14],
            'sSalesName': row[15],
            'sSalesGroupName': row[16],
            'sColorBorder': row[17],
            'nOverTime': row[18],
            'uppTrackJobGUID': row[20],
            'sLocation': row[21],
            'sWorkingProcedureNameLast': row[22],
            'sWorkingProcedureNameNext': row[23],
            'dReplyDate': row[24],
            'dDeliveryDate': row[25],
            'sRemark': row[26]
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData


# 通过机台的类型查找机台号
def SearchEquipment(sEquipmentModelName):
    ReturnData = []
    sSQL = SearchEquipmentSQL(sEquipmentModelName)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'sEquipmentNo': row[1],
            'sEquipmentName': row[2],
            'uemEquipmentGUID': row[3],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData


# 更新数据
def Data_DXNoPlan(sWorkingProcedureName):
    # print(args)
    sSQL = NoDXPlanSQL(sWorkingProcedureName)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    returnData2 = []
    while row:
        dictVar = {
            'sBorderColor': row[0],
            'sCardNo': row[1],
            'sMaterialNo': row[2],
            'sMaterialLot': row[3],
            'sColorNo': row[4],
            'nFactInPutQty': row[5],
            'sCustomerName': row[6],
            'sSalesGroupName': row[7],
            'nTemp': row[8],
            'nSpeed': row[9],
            'nTime': row[10],
            'sProductWidth': row[11],
            'sProductGMWT': row[12],
            'sColorBorder': row[13],
            'uppTrackJobGUID': row[14],
            'sWorkingProcedureName': str(row[15]),
            'sLocation': str(row[16]),
        }
        # print('bbbbbffdsd')
        # print(dictVar)
        returnData2.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData2


# 预排子表数据
def Data_DXPlan(sEquipmentID):
    sSQL = DXPlanSQL(sEquipmentID)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    returnData = []
    equipmentList = []
    while row:
        dictVar = {
            'sBorderColor': row[0],
            'sCardNo': row[1],
            'sMaterialNo': row[2],
            'sMaterialLot': row[3],
            'sColorNo': row[4],
            'nFactInPutQty': row[5],
            'sCustomerName': row[6],
            'sSalesGroupName': row[7],
            'nTemp': row[8],
            'nSpeed': row[9],
            'nTime': row[10],
            'sProductWidth': row[11],
            'sProductGMWT': row[12],
            'sColorBorder': row[13],
            'uppTrackJobGUID': row[14],
            'sWorkingProcedureNameCurrent': row[15],
            'sLocation': row[16],
            'sEquipmentNo': row[17],
            'nHDRID': row[18],
            'nRowNumber': row[19],
        }
        equipmentDict = {
            'nHDRID': row[18],
        }
        if equipmentDict not in equipmentList:
            equipmentList.append(equipmentDict)
        # print(dictVar)
        # print(dictVar)
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData


# 生管导入EXCEL
def importData_PMC(Data):
    cursor = connect.cursor()
    INSERTData = []
    sql = InsertImportData()
    for innerData in Data:
        sType = innerData['sType']
        dData = innerData['Data']
        e = 0;
        for i in dData:
            # print('----------------')
            if IsInPMCPlan(i['TrackJob']) != True:
                sList = (sType, e, i['TrackJob'], GetDate(), i['加急'])
                INSERTData.append(sList)
                e += 1
    cursor.executemany(sql, INSERTData)
    connect.commit()
    cursor.close()
    # print(sql)
    print('导入成功')