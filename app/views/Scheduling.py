# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect
from app.sql.ProductionScheduling import GETSchedulingSQL, GetSchedulingDtlSQL
import re

base = declarative_base()
# 236
session = sessionmaker(bind=engine_253)
ses = session()

def GetSchedulingData(args):
    sVarArgs = ''.join(args)
    sSQL = GETSchedulingSQL(sVarArgs)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    returnData = []
    while row:
        dictVar = {
            'sBorderColor' : row[0],
            'sCardNo' : row[1],
            'sMaterialNo' : row[2],
            'sMaterialLot' : row[3],
            'sColorNo' : row[4],
            'nFactInPutQty' : row[5],
            'sCustomerName' : str(row[6]),
            'sSalesName' : str(row[7]),
            'sSalesGroupName' : str(row[8]),
            'nPSTime' : str(row[9]),
            'nSETime' : str(row[10]),
            'nPSSpeed' : str(row[11]),
            'nSESpeed' : str(row[12]),
            'nPS2Temp' : str(row[13]),
            'nSETemp' : str(row[14]),
            'sProductWidth' : str(row[15]),
            'sProductGMWT' : str(row[16]),
            'sColorBorder' : str(row[17]),
        }
        # print(dictVar)
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData


def GetSchedulingDtlData():
    print('------------------------------')
    sSQL = GetSchedulingDtlSQL()
    print(sSQL)
    cursor = connect.cursor()
    cursor.execute(sSQL)
    row = cursor.fetchone()
    returnData = []
    equipmentList = []
    nBigID = 0
    while row:
        dictVar = {
            'ID' : row[0],
            'nHDRID' : row[1],
            'nRowNumber' : str(row[2]),
            'sBorderColor' : str(row[3]),
            'sCardNo' : str(row[4]),
            'sMaterialNo' : str(row[5]),
            'sMaterialLot' : str(row[6]),
            'sColorNo' : str(row[7]),
            'nFactInPutQty' : str(row[8]),
            'sCustomerName' : str(row[9]),
            'sSalesName' : str(row[10]),
            'sSalesGroupName' : str(row[11]),
            'nPSTime' : str(row[12]),
            'nSETime' : str(row[13]),
            'nPSSpeed' : str(row[14]),
            'nSESpeed' : str(row[15]),
            'nPS2Temp' : str(row[16]),
            'nSETemp' : str(row[17]),
            'sProductWidth' : str(row[18]),
            'sProductGMWT' : str(row[19]),
            'sColorBorder' : str(row[20]),
        }
        equipmentDict = {
            'nHDRID' : row[1],
        }
        if equipmentDict not in equipmentList:
            equipmentList.append(equipmentDict)
        nBigID = row[0]
        # print(dictVar)
        # print(dictVar)
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()

    for i in range(1,6):
        Dict3 = {
            'nHDRID' : i,
        }
        if Dict3 not in equipmentList:
            nBigID += 1
            Dict4 = {
            'ID' : nBigID,
            'sCardNo' : '空机台',
            'nHDRID' : i,
            }
            returnData.append(Dict4)
    return returnData