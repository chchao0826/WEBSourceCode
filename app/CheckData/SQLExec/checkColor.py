# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect
from app.CheckData.SQL.checkColor import sCheckColorSql



import re


base = declarative_base()
# 236
session = sessionmaker(bind=engine)
ses = session()


# 研发数据对比执行
def ColorData(*args):
    sSQL = sCheckColorSql()
    cursor = connect.cursor()
    # 创建一个游标对象,python里的sql语句都要通过cursor来执行
    cursor.execute(sSQL)
    # 执行sql语句
    row = cursor.fetchone()
    sList = []
    while row:
        sDict = {
            'sColorNo' : row[0],
            'sColorName' : row[1],
            'sColorCode' : row[2],
            'sIsCheck' : row[3],
            'sIsDelete' : row[4],
        }
        sList.append(sDict)

    return sList


