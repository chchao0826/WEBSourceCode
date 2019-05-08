# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect
from app.sql.CheckFabric import GETMaterial, GETFabric, GETDefectType, GETDefect, GETEquipment, GETUserName, ViewTitle, Fabric, OtherDefect, IsHaveuppTrackJobGUID, IsInsertDtl, IsPopupBeginOrSearch, Updatetable, UpdateDefect, SearchCard
import re

base = declarative_base()
# 236
session = sessionmaker(bind=engine_253)
ses = session()

# 机台状态
def GetDetail(sCardNo):
    # 执行SQL语句转为List-详细
    returnData = []
    SQL = GETMaterial(sCardNo)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        # print(row)
        dictVar = {
            'sOrderNo' : row[0],
            'sMaterialNo' : row[1],
            'sCustomerName' : row[2],
            'sColorNo' : row[3],
            'sProductWidth' : row[4],
            'sLocation' : row[5],
            'uppTrackJobGUID' : str(row[6]),
            'usdOrderLotGUID' : str(row[7]),
            'ummMaterialGUID' : str(row[8]),
            'utmColorGUID' : str(row[9]),
            'upsWorkFlowCardGUID' : str(row[10]),
        }
        # print(dictVar)
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 机台状态
def SearchCardNo(sCardNo):
    # 执行SQL语句转为List-详细
    returnData = []
    SQL = SearchCard(sCardNo)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        # print(row)
        dictVar = {
            'sOrderNo' : row[0],
            'sMaterialNo' : row[1],
            'sCustomerName' : row[2],
            'sColorNo' : row[3],
            'sProductWidth' : row[4],
            'sLocation' : row[5],
            'uppTrackJobGUID' : str(row[6]),
            'usdOrderLotGUID' : str(row[7]),
            'ummMaterialGUID' : str(row[8]),
            'utmColorGUID' : str(row[9]),
            'upsWorkFlowCardGUID' : str(row[10]),
        }
        # print(dictVar)
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData


# 配检详细信息
def GETFabricIn(sCardNo):
    returnData = []
    SQL = GETFabric(sCardNo)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        # print(row)
        dictVar = {
            'sFabricNo': row[0],
            'sMaterialNo': row[1],
            'sMaterialName': row[2],
            'sMaterialLot': row[3],
            'nFactInputQty': row[4],
            'nFactInputLen': row[5],
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 机台信息
def GetEquipment():
    returnData = []
    SQL = GETEquipment()
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        # print(row)
        dictVar = {
            'sEquipmentNo': row[0],
            'sEquipmentName': row[1]
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 查询疵点类别
def GetDefectType():
    returnData = []
    SQL = GETDefectType()
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        # print(row)
        dictVar = {
            'ID':row[0],
            'sDefectTypeName':row[1]
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 根据疵点类别获取疵点
def GetDefect(sTypeID):
    returnData = []
    SQL = GETDefect(sTypeID)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        # print(row)
        dictVar = {
            'sDefectNameCN':row[0],
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 得到用户姓名
def GetUserName():
    returnData = []
    SQL = GETUserName()
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        # print(row)
        dictVar = {
            'sUserID':row[0],
            'sUserName':row[1],
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 表头资料
def GetViewTitle(sCardNo):
    returnData = []
    SQL = ViewTitle(sCardNo)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        # print(row)
        dictVar = {
            'sCardNo' : row[0],
            'sColorNo' : row[1],
            'sMaterialNo' : row[2],
            'sMaterialLot' : row[3],
            'sCustomerName' : row[4],
            'sMaterialNoProduct' : row[5],
            'sCustomerOrderNo' : row[6],


        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 疋号的第一行资料
def GetViewFabric(sCardNo):
    returnData = []
    SQL = Fabric(sCardNo)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        dictVar = {
            'sFabricNo' : row[0],
            'nLengthYard' : row[1],
            'nLengthMeter' : row[2], 
            'nDensity' : row[3],
            'nWidth' : row[4],
            'nGMWTLeft' : row[5],
            'nGMWTInner' : row[6],
            'nGMWTRight' : row[7],
            'One' : row[8],
            'Two' : row[9],
            'three' : row[10],
            'Four' : row[11],
            'SUMScore' : row[12],
            'nMaxScore' : row[13],
            'sMainDefectName' : row[14],
            'sRemark' : row[15],
            'sGrade' : row[16],
            'sDefectTypeName' : row[17],
            'nSite' : row[18],
            'nScore' : row[19],
            'nCount' : row[20],
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 其他资料
def GetViewOtherDefect(sFabricNo):
    returnData = []
    SQL = OtherDefect(sFabricNo)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        dictVar = {
            'sCardNo' : row[0],
            'sFabricNo' : row[1],
            'sDefectTypeName' : row[2],
            'nSite' : row[3],
            'nScore' : row[4]
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 判断该工段是否进行插入
def ISHaveuppTrackJobGUID(uppTrackJobGUID):
    returnData = []
    SQL = IsHaveuppTrackJobGUID(uppTrackJobGUID)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        dictVar = {
            'iFlag' : row[0],
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 判断Dtl数据是否插入
def ISInsertDtl(uppTrackJobGUID, sFabricNo):
    returnData = []
    SQL = IsInsertDtl(uppTrackJobGUID, sFabricNo)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        dictVar = {
            'iFlag' : row[0],
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData

# 点击查询后弹出窗口判断(开工,查询信息)
def ISPopupBeginOrSearch(sCardNo):
    returnData = []
    returnData2 = []
    SQL = IsPopupBeginOrSearch(sCardNo)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    i = 0
    # 读取查询结果
    while row:
        if row[0] == '已完成':
            iFlag = 'iFlag' + str(0)
        else:
            iFlag = 'iFlag' + str(1)
        dictVar = {
            iFlag : row[0],
        }
        i += 1
        if dictVar not in returnData:
            print(returnData)
            returnData.append(dictVar)
        if row[0] == '已完成':
            dictDict = {
                'sType':row[0],
                'tInspectTime':row[1],
                'sWorkingProcedureName':row[2],
                'nRowNumber':row[3],
                'sCardNo' : row[4],
                'ID' : row[5],
            }
            returnData2.append(dictDict)
        row = cursor.fetchone()
    cursor.close()
    return returnData, returnData2

def UPDATETable(ipbCommonDataHalfInspectHdrID):
    returnData1 = []
    returnData2 = []
    SQL = Updatetable(ipbCommonDataHalfInspectHdrID)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        dictVar1 = {
            'tInspectTime' : row[0],
            'sMaterialLot' : row[2],
            'nLengthYard' : row[3],
            'nLengthMeter' : row[4],
            'sGrade' : row[13],
            'nWidth' : row[5],
            'sMainDefectName' : row[14],
            'sRemark' : row[10],
            'ID' : row[11],
        }
        returnData1.append(dictVar1)

        dictVar2 = {
            'sFabricNo2' :  row[1],
            'nLength' : row[3],
            'nWidth' : row[5],
            'nDensity' : row[6],
            'nGMWTLeft' : row[7],
            'nGMWTInner' : row[8],
            'nGMWTRight' : row[9],
            'sGrade' : row[13],
            'sDefect' : row[14],
            'sRemark' : row[10],
            'ID' : row[11],

        }
        returnData2.append(dictVar2)


        # row = cursor.fetchone(dictVar1)
        row = cursor.fetchone()
    cursor.close()
    return returnData1, returnData2


def UPDATETableDefect(ipbCommonDataHalfInspectDtlID):
    returnData1 = []
    SQL = UpdateDefect(ipbCommonDataHalfInspectDtlID)
    # print(SQL)
    cursor = connect_253.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(SQL)
    # 执行sql语句
    row = cursor.fetchone()
    # 读取查询结果
    while row:
        dictVar1 = {
            'iNumber' : row[0],
            'sDefectTypeName' : row[1],
            'nScore' : row[2],
            'nSite' : row[3],
            'ID' : row[4],
        }
        returnData1.append(dictVar1)
        row = cursor.fetchone()
    cursor.close()
    return returnData1

