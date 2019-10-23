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

# CheckData
from app.CheckData import CheckData as checkData_blueprint
app.register_blueprint(checkData_blueprint, url_prefix = '/CheckData/')

# # CheckFabric
# from app.CheckFabric import CheckFabric as CheckFabric_blueprint
# app.register_blueprint(CheckFabric_blueprint, url_prefix = '/CheckFabric/')



