# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine, connect

from app.KanBan.PlanDX.SQL.PlanDX import SQL_PlanDX, SearchFunSql

import time

import re

# 236
base = declarative_base()
session = sessionmaker(bind=engine)
ses = session()


# 生管整理预排SQL
def Data_PlanDX(sEquipmentNo):
    print(sEquipmentNo)
    ReturnData = []
    sSQL = SQL_PlanDX(sEquipmentNo)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'nRowNumber': row[0],
            'sEquipmentNo': row[1],
            'tPlanTime': row[2],
            'sOverTime': row[3],
            'sCustomerName': row[4],
            'sLocation': row[5],
            'sMaterialNo': row[6],
            'sMaterialLot': row[7],
            'sCardNo': row[8],
            'sColorNo': row[9],
            'nFactInputQty': row[10],
            'sWorkingProcedureNameLast': row[11],
            'sWorkingProcedureNameCurrent': row[12],
            'sWorkingProcedureNameNext': row[13],
            'dReplyDate': row[14],
            'dDeliveryDate': row[15],
            'nTime': row[16],
            'sSalesGroupName': row[17],
            'sRemark': row[18],
            'sLabel': row[19],
            'tFactEndTime': row[20],
            'tUpdateTime': row[21],
            'nPMCNumber': row[22],
            'sPMCType': row[23],
            'uppTrackJobGUID': row[24],
            'sOrderNo': row[25]
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData


# 搜索数据
def SearchFun(sSearchValue):
    print(sSearchValue)
    ReturnData = []
    sSQL = SearchFunSql(sSearchValue)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    sEquipmentNo = ''
    while row:
        sEquipmentNo = row[1]
        dictVar = {
            'nRowNumber': row[0],
            'sEquipmentNo': row[1],
            'tPlanTime': row[2],
            'sOverTime': row[3],
            'sCustomerName': row[4],
            'sLocation': row[5],
            'sMaterialNo': row[6],
            'sMaterialLot': row[7],
            'sCardNo': row[8],
            'sColorNo': row[9],
            'nFactInputQty': row[10],
            'sWorkingProcedureNameLast': row[11],
            'sWorkingProcedureNameCurrent': row[12],
            'sWorkingProcedureNameNext': row[13],
            'dReplyDate': row[14],
            'dDeliveryDate': row[15],
            'nTime': row[16],
            'sSalesGroupName': row[17],
            'sRemark': row[18],
            'sLabel': row[19],
            'tFactEndTime': row[20],
            'tUpdateTime': row[21],
            'nPMCNumber': row[22],
            'sPMCType': row[23],
            'uppTrackJobGUID': row[24],
            'sOrderNo': row[25]
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData, sEquipmentNo