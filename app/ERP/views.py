# -*- coding: utf-8 -*-
from . import ERP
from flask import Flask, render_template, jsonify, request
import json


# 试布追踪记录
@ERP.route('/CheckData/JS')
def CheckData_JS():
    return render_template('ERP/CheckData_JS_URL.html')


# 工厂平面图
@ERP.route('/KanBan/FloorPlan')
def KanBan_FloorPlan():
    return render_template('ERP/KanBan_FloorPlan.html')

