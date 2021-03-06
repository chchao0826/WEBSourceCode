from flask import Flask

app = Flask(__name__)
app.debug = True


# Index
from app.Home import Home as home_blueprint
app.register_blueprint(home_blueprint)


# kanban
from app.KanBan import KanBan as kanban_blueprint
app.register_blueprint(kanban_blueprint, url_prefix = '/KanBan/')


# plan
from app.Plan import Plan as plan_blueprint
app.register_blueprint(plan_blueprint, url_prefix = '/Plan/')


# plan
from app.PlanDye import PlanDye as planDye_blueprint
app.register_blueprint(planDye_blueprint, url_prefix = '/PlanDye/')


# CheckData
from app.CheckData import CheckData as checkData_blueprint
app.register_blueprint(checkData_blueprint, url_prefix = '/CheckData/')


# ERP
from app.ERP import ERP as ERP_blueprint
app.register_blueprint(ERP_blueprint, url_prefix = '/ERP/')


# Chart
from app.Chart import Chart as Chart_blueprint
app.register_blueprint(Chart_blueprint, url_prefix = '/Chart/')


# # CheckFabric
# from app.CheckFabric import CheckFabric as CheckFabric_blueprint
# app.register_blueprint(CheckFabric_blueprint, url_prefix = '/CheckFabric/')



