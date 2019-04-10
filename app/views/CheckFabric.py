# -*-coding:utf-8-*-
from flask import render_template, Flask, request
from sqlalchemy import or_, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, query
from app.config import engine_253, connect_253, engine, connect
from app.sql.CheckFabric import GETMaterial, GETFabric, GETDefectType, GETDefect, GETEquipment
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
            'sOrderNo':row[0],
            'sMaterialNo':row[1],
            'sCustomerName':row[2],
            'sColorNo':row[3],
            'sProductWidth':row[4],
            'sLocation':row[5],
        }
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
            'sFabricNo':row[0],
            'sMaterialNo':row[1],
            'sMaterialName':row[2],
            'sMaterialLot':row[3],
            'nFactInputQty':row[4],
            'nFactInputLen':row[5],
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
            'sEquipmentNo':row[0],
            'sEquipmentName':row[1]
        }
        returnData.append(dictVar)
        row = cursor.fetchone()
    cursor.close()
    return returnData