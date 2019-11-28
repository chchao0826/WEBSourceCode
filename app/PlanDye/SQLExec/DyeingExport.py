# -*- coding:utf-8 -*-
# 染色预排导出SQL执行

from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.PlanDye.SQL.Export import ExportSQL
from app.config import engine, connect


# 预排导出数据
def DyeingData():
    sSQL = ExportSQL()
    # print(sSQL)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    returnData = []
    print(sSQL)
    while row:
        dictVar = {
            'sEquipmentNo' : row[0],
            'sPlanEquipmentNo' : row[1],
            'sOverTime' : row[2],
            'sCustomerName' : row[3],
            'sCardNo' : row[4],
            'sMaterialNo' : row[5],
            'sMaterialLot' : row[6],
            'sColorNo' : row[7],
            'nFactInputQty' : row[8],
            'sWorkingProcedureNameLast' : row[9],
            'sWorkingProcedureNameCurrent' : row[10],
            'sWorkingProcedureNameNext' : row[11],
            'nDyeingTime' : row[12],
            'sLocation' : row[13],
            'sRemark' : row[14],
            'sOrderNo' : row[15],
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    print(returnData)
    cursor.close()
    return returnData