# -*- coding:utf-8 -*-
# 染色预排SQL执行

from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.PlanDye.SQL.DyeSql import allDyeingSql, DyeingEquipmentSql, IDGetDataSql, IDGetEquipmentSql
from app.config import engine, connect



# # 236
# base = declarative_base()
# session = sessionmaker(bind=engine)
# ses = session()


# 预排数据
def DyeingData(sEquipmentModelName):
    ReturnData = []
    sSQL = allDyeingSql(sEquipmentModelName)
    print(sSQL)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'sEquipmentNo' : row[0],
            'ID' : row[1],
            'sOverTime' : row[2],
            'sCardNo' : row[3],
            'sMaterialNo' : row[4],
            'sMaterialLot' : row[5],
            'sColorNo' : row[6],
            'sWorkingProcedureNameLast' : row[7],
            'sWorkingProcedureNameCurrent' : row[8],
            'nFactInputQty' : row[9],
            'nDyeingTime' : row[10],
            'sCustomerName' : row[11],
            'sSalesGroupName' : row[12],
            'sSalesName' : row[13],
            'sColorCode' : row[14],
            'nRowNumber' : row[15],
            'nDyeingCount' : row[16],
            'sIsStart' : row[17],
            'sPSColor' : row[18],
            'sDyeingCount' : row[19],
            'sDyeingColor' : row[20],
            'sWorkCode' : row[21],
            'sIsHYS' : row[22],
            'bISCheck' : row[23],
            'sOverColor' : row[24],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData


# 机台列表
def DyeingEquipment(sEquipmentModelName):
    ReturnData = []
    sSQL = DyeingEquipmentSql(sEquipmentModelName)
    print(sSQL)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'ID' : row[0],
            'sEquipmentNo' : row[1],
            'sEquipmentName' : row[2],
            'nCardCount' : row[3],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData


# 预排数据
def IDGetData(ID):
    ReturnData = []
    sSQL = IDGetDataSql(ID)
    print(sSQL)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'sEquipmentNo' : row[0],
            'ID' : row[1],
            'sOverTime' : row[2],
            'sCardNo' : row[3],
            'sMaterialNo' : row[4],
            'sMaterialLot' : row[5],
            'sColorNo' : row[6],
            'sWorkingProcedureNameLast' : row[7],
            'sWorkingProcedureNameCurrent' : row[8],
            'nFactInputQty' : row[9],
            'nDyeingTime' : row[10],
            'sCustomerName' : row[11],
            'sSalesGroupName' : row[12],
            'sSalesName' : row[13],
            'sColorCode' : row[14],
            'nRowNumber' : row[15],
            'nDyeingCount' : row[16],
            'sIsStart' : row[17],
            'sPSColor' : row[18],
            'sDyeingCount' : row[19],
            'sDyeingColor' : row[20],
            'sWorkCode' : row[21],
            'sIsHYS' : row[22],
            'bISCheck' : row[23],
            'sOverColor' : row[24],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData



# 机台列表
def IDGetEquipment(ID):
    ReturnData = []
    sSQL = IDGetEquipmentSql(ID)
    print(sSQL)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'ID' : row[0],
            'sEquipmentNo' : row[1],
            'sEquipmentName' : row[2],
            'nCardCount' : row[3],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData