
# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect
# 故障看板
from app.KanBan.Service.SQL.EquipmentService import equipmentServiceSQL

import re


base = declarative_base()
# 236
session = sessionmaker(bind=engine)
ses = session()


# 设备检修SQL执行
def equipmentServiceData(*args):
    nPage = ''.join(args)
    nThisPage = 1
    if nPage == '' or nPage == None:
        nThisPage = 1
    else:
        nThisPage = nPage
    cursor = connect.cursor()
    sSql = equipmentServiceSQL()
    cursor.execute(sSql)
    row = cursor.fetchone()
    sList = []
    nCount = 0
    nAllPage = 0
    while row:
        # print(row)
        sDict = {
            'sServiceNo' : row[0],
            'sTime' : row[1],
            'sWorkCentreName' : row[2],
            'sReportName' : row[3],
            'sServiceType' : row[4],
            'sEquipmentName' : row[5],
            'sEquipmentNo' : row[6],
            'sEquipmentDetailType' : row[7],
            'sEquipmentDetail' : row[8],
            'sServiceName' : row[9],
            'sFaultReason' : row[10],
            'sServiceStatus' : row[11],
            'sStatus' : row[12],
        }
        if nCount // 10 == int(nThisPage):
            sList.append(sDict)
        nAllPage = nCount // 10
        nCount += 1
        row = cursor.fetchone()
    cursor.close()
    return sList, nCount, nAllPage

