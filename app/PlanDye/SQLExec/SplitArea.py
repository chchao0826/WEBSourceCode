# -*- coding:utf-8 -*-
# 染色预排 划分分组 SQL执行

from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.PlanDye.SQL.SplitAreaSql import IDGetCheckDataSql, IDGetNotCheckDataSql
from app.config import engine, connect


# # 236
# base = declarative_base()
# session = sessionmaker(bind=engine)
# ses = session()


# 预排数据
def DyeingData(sSQL):
    ReturnData = []
    # print(sSQL)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    while row:
        dictVar = {
            'sEquipmentNo': row[0],
            'ID': row[1],
            'sOverTime': row[2],
            'sCardNo': row[3],
            'sMaterialNo': row[4],
            'sMaterialLot': row[5],
            'sColorNo': row[6],
            'sWorkingProcedureNameLast': row[7],
            'sWorkingProcedureNameCurrent': row[8],
            'nFactInputQty': row[9],
            'nDyeingTime': row[10],
            'sCustomerName': row[11],
            'sSalesGroupName': row[12],
            'sSalesName': row[13],
            'sColorCode': row[14],
            'nRowNumber': row[15],
            'sType': row[16],
            'sIsStart': row[17],
            'sPSColor': row[18],
            'sDyeingCount': row[19],
            'sDyeingColor': row[20],
            'sWorkCode': row[21],
            'sIsHYS': row[22],
            'bISCheck': row[23],
            'sOverColor': row[24],
            'sWorkingProcedureNameNext': row[25],
            'sIsStart': row[26],
            'dReplyDate': row[27],
            'dDeliveryDate': row[28],
            'sRemark': row[29],
            'sIsRush': row[30],
            'sISHasHYS': row[31],
            'sISHasDX': row[32],
            'sIsRushColor': row[33],
        }
        ReturnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return ReturnData


# 未预排数据执行
def IDGetCheckData(sEquipmentNo):
    sSql = IDGetCheckDataSql(sEquipmentNo)
    returnData = DyeingData(sSql)
    return returnData


# 已预排数据执行
def IDGetNotCheckData(sEquipmentNo):
    sSql = IDGetNotCheckDataSql(sEquipmentNo)
    returnData = DyeingData(sSql)
    return returnData
