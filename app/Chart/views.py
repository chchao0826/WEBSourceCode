# -*- coding: utf-8 -*-
#  图形看板
from . import Chart
from flask import Flask, render_template, jsonify, request
from app.Chart.SQLEXEC.DXChart import DXDone, ReturnDXTop3Data
import json


# 看板
@Chart.route('/DX/')
def Chart_DX():
    return render_template('Chart/Chart_DX.html')


# 达成率
@Chart.route('/DX/DoneChart')
def Chart_DX_Done():
    DXDoneData = DXDone()
    DXDoneDataJson = json.dumps(DXDoneData, indent=2, ensure_ascii=False)
    return DXDoneDataJson


# 定型上部的其他三个数据
@Chart.route('/DX/Top3Chart')
def Chart_DX_Top3():
    DXTop3Data = ReturnDXTop3Data()
    abnormalDATA = DXTop3Data[0]
    stateDATA = DXTop3Data[1]
    startUpDATA = DXTop3Data[2]
    returnData = []
    returnData.append({
        'Type' : 'abnormal',
        'Data' : abnormalDATA,
    })
    returnData.append({
        'Type' : 'state',
        'Data' : stateDATA,
    })
    returnData.append({
        'Type' : 'startUp',
        'Data' : startUpDATA,
    })


    returnDataJson = json.dumps(returnData, indent=2, ensure_ascii=False)
    return returnDataJson
