# -*- coding: utf-8 -*-
from . import ERP
from flask import Flask, render_template, jsonify, request
import json


# 看板
# 看板_工厂平面图
@ERP.route('/KanBan/FloorPlan')
def KanBan_FloorPlan():
    return render_template('ERP/KanBan_FloorPlan.html')


# 看板_技术部看板
@ERP.route('/KanBan/JS')
def KanBan_JS():
    return render_template('ERP/KanBan_JS.html')


# 看板_染色预排看板_所有
@ERP.route('/KanBan/PlanDyeAll')
def KanBan_PlanDyeAll():
    return render_template('ERP/KanBan_PlanDyeAll.html')


# 看板_染色预排看板_业务
@ERP.route('/KanBan/PlanDyeSale')
def KanBan_PlanDyeSale():
    return render_template('ERP/KanBan_PlanDyeSale.html')


# 预排_定型预排看板
@ERP.route('/KanBan/PlanZL')
def KanBan_PlanZL():
    return render_template('ERP/KanBan_PlanZL.html')


# 预排_定型预排_定型
@ERP.route('/Plan/PlanDX_DX')
def Plan_PlanDX_DX():
    return render_template('ERP/Plan_PlanDX_DX.html')


# 预排_定型预排_生管
@ERP.route('/Plan/PlanDX_PMC')
def Plan_PlanDX_PMC():
    return render_template('ERP/Plan_PlanDX_PMC.html')


# 预排_染色预排_生管
@ERP.route('/Plan/PlanDye_PMC')
def Plan_PlanDye_PMC():
    return render_template('ERP/Plan_PlanDye_PMC.html')


# 试布追踪记录
@ERP.route('/CheckData/JS')
def CheckData_JS():
    return render_template('ERP/CheckData_JS_URL.html')
