# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect
from app.sql.ProductionScheduling import GETSchedulingSQL, GetSchedulingDtlSQL
from app.sql.SchedulingZL_PMC import GetSchedulingSQL_ZL_PMC, GetSchedulingSQL_ZL_PMCHDR, SearchAllCard
from app.sql.SearchEquipmentNo import SearchEquipmentNoSQL
from app.sql.Color import colorSql


import re

base = declarative_base()
# 236
session = sessionmaker(bind=engine_253)
ses = session()

# 预排数据
def GetSchedulingData(args):
    # print(args)
    sVarArgs = ''.join(args)
    sSQL = GETSchedulingSQL(sVarArgs)
    # print(sSQL)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    returnData = []
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
        # print(dictVar)
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 预排子表数据
def GetSchedulingDtlData():
    sSQL = GetSchedulingDtlSQL()
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    returnData = []
    equipmentList = []
    nBigID = 0
    while row:
        dictVar = {
            'sBorderColor' : row[0],
            'sCardNo' : row[1],
            'sMaterialNo' : row[2],
            'sMaterialLot' : row[3],
            'sColorNo' : row[4],
            'nFactInPutQty' : row[5],
            'sCustomerName' : row[6],
            'sSalesGroupName' : row[7],
            'nTemp' : row[8],
            'nSpeed' : row[9],
            'nTime' : row[10],
            'sProductWidth' : row[11],
            'sProductGMWT' : row[12],
            'sColorBorder' : row[13],
            'uppTrackJobGUID' : row[14],
            'sWorkingProcedureNameCurrent' : row[15],
            'sLocation' : row[16],
            'sEquipmentNo' : row[17],
            'nHDRID' : row[18],
            'nRowNumber' : row[19],
        }
        equipmentDict = {
            'nHDRID': row[18],
        }
        if equipmentDict not in equipmentList:
            equipmentList.append(equipmentDict)
        nBigID = row[19]
        # print(dictVar)
        # print(dictVar)
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    for i in range(1, 6):
        Dict3 = {
            'nHDRID': i,
        }
        if Dict3 not in equipmentList:
            nBigID += 1
            Dict4 = {
                'ID': nBigID,
                'nHDRID': i,
                'nRowNumber': i,
                'sBorderColor': '#fff',
                'sCardNo': '空机台',
                'sMaterialNo': '',
                'sMaterialLot': '',
                'sColorNo': '',
                'nFactInPutQty': '',
                'sCustomerName': '',
                'sSalesName': '',
                'sSalesGroupName': '',
                'nTemp': '',
                'nSpeed': '',
                'nTime': '',
                'sProductWidth': '',
                'sProductGMWT': '',
                'sColorBorder': '',
                'uppTrackJobGUID': '',
                'sWorkingProcedureName': ''
            }
            returnData.append(Dict4)
    return returnData

# 生管整理预排SQL
def SchedulingDataZL_PMC(sWorkingProcedureName, sWorkingProcedureName2):
    ReturnData = []
    # print(sWorkingProcedureName)
    sSQL = GetSchedulingSQL_ZL_PMC(sWorkingProcedureName, sWorkingProcedureName2)
    # print(sSQL)
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
            'sRemark':row[24],
            'sWorkingProcedureNameLast':row[25],
            'sWorkingProcedureNameNext':row[26],
            'dReplyDate':row[27],
            'dDeliveryDate':row[28],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData

# 生管整理预排主表
def SchedulingSQL_ZL_PMCHDR(sType):
    ReturnData = []
    sSQL = GetSchedulingSQL_ZL_PMCHDR(sType)
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
            'sRemark':row[23],
            'sWorkingProcedureNameLast':row[24],
            'sWorkingProcedureNameNext':row[25],
            'dReplyDate':row[26],
            'dDeliveryDate':row[27],
            'sType':sType,
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
            'sWorkingProcedureNameLast':'',
            'sWorkingProcedureNameNext':'',
            'dReplyDate':'',
            'dDeliveryDate':'',
        }
        ReturnData.append(dictVar)
    cursor.close()
    return ReturnData

# Search其他卡号
def SearchOtherCard(sCardNo, sWorkingProcedureName):
    ReturnData = []
    sSQL = SearchAllCard(sCardNo, sWorkingProcedureName)
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
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData

# 色号对应颜色
def Color():
    ReturnData = []
    cursor = connect.cursor()
    cursor.execute(colorSql)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'ID': row[0],
            'Page': row[1],
            'Color': row[2],
            'No': row[3],
            'Name': row[4],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData

# 通过机台的类型查找机台号
def SearChEquipment(sEquipmentModelName):
    ReturnData = []
    sSQL = SearchEquipmentNoSQL(sEquipmentModelName)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'sEquipmentNo':row[1],
            'sEquipmentName':row[2],
            'uemEquipmentGUID':row[3],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData