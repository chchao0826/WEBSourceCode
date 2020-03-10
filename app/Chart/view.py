# -*- coding: utf-8 -*-
#  图形看板
from . import Chart
from flask import Flask, render_template, jsonify, request
import json


# 看板
@Chart.route('/DX')
def KanBan_FloorPlan():
    return render_template('ERP/KanBan_FloorPlan.html')

