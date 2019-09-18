from flask import Flask

app = Flask(__name__)
app.debug = True

# Index
from app.home import home as home_blueprint
app.register_blueprint(home_blueprint)

# kanban
from app.kanban import kanban as kanban_blueprint
app.register_blueprint(kanban_blueprint, url_prefix = '/kanban/')


# plan
from app.plan import plan as plan_blueprint
app.register_blueprint(plan_blueprint, url_prefix = '/plan/')

# # CheckData
# from app.CheckData import CheckData as CheckData_blueprint
# app.register_blueprint(CheckData_blueprint, url_prefix = '/CheckData/')

# # CheckFabric
# from app.CheckFabric import CheckFabric as CheckFabric_blueprint
# app.register_blueprint(CheckFabric_blueprint, url_prefix = '/CheckFabric/')



