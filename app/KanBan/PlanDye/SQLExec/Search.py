# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect
# 故障看板
from app.KanBan.PlanDye.SQL.Search import SearchSql

import re
import math


base = declarative_base()
# 236
session = sessionmaker(bind=engine)
ses = session()


# 搜索SQL执行
def SearchExec(inputValue, sPage):
    nPage = int(sPage)
    cursor = connect.cursor()
    sSql = SearchSql(inputValue)
    cursor.execute(sSql)
    row = cursor.fetchone()
    sList = []
    nAllNum = 0
    while row:
        sDict = {
            'sCardNo' : row[0],
            'sMaterialNo' : row[1],
            'sOrderNo' : row[2],
            'sEquipmentNo' : row[3],
            'sCheckType' : row[4],
            'ID' : row[5],
            'nHDRID' : row[6],
        }
        nAllNum += 1

        if nAllNum > (nPage - 1) * 10 and nAllNum <= nPage * 10:
            sList.append(sDict)
        row = cursor.fetchone()
    cursor.close()

    nPageNumber = math.ceil(nAllNum / 11)

    return sList, nPageNumber

