# -*-coding:utf-8-*-
from app.KanBan import KanBan
from flask import render_template, Flask, request

from app.KanBan.PlanDX.Models.DX import DXKanBanData, DXKanBanChartData
from app.Plan.Models.plan import GetEquipment

import json


# 定型看板
@KanBan.route('/DX/')
def DXKanBan():
    returnData = DXKanBanData()
    EqList = GetEquipment('整理')
    print(returnData)
    print(EqList)
    return render_template('KanBan/plan_zl.html', returnData=returnData, equipmentData=EqList)


# 定型看板-山积图
@KanBan.route('/DX/chart')
def DXKanBan_Chart():
    EqList = GetEquipment('整理')
    DXKanBanChart = DXKanBanChartData()
    print(EqList)
    print('================')
    print(DXKanBanChart)
    return render_template('kanban/plan_zl_chart.html', EqList=EqList, DXKanBanChart=DXKanBanChart)

