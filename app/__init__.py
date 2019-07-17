from flask import Flask

app = Flask(__name__)
app.debug = True

# KanBan
from app.KanBan import KanBan as KanBan_blueprint
app.register_blueprint(KanBan_blueprint, url_prefix = '/KanBan/')

# CheckFabric
from app.CheckFabric import CheckFabric as CheckFabric_blueprint
app.register_blueprint(CheckFabric_blueprint, url_prefix = '/CheckFabric/')

# Scheduling
from app.Scheduling import Scheduling as Scheduling_blueprint
app.register_blueprint(Scheduling_blueprint, url_prefix = '/Scheduling/')

# CheckData
from app.CheckData import CheckData as CheckData_blueprint
app.register_blueprint(CheckData_blueprint, url_prefix = '/CheckData/')

# Index
from app.home import home as home_blueprint
app.register_blueprint(home_blueprint)
