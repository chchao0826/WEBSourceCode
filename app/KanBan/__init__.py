# coding:utf8

from flask import Blueprint

KanBan = Blueprint('KanBan',__name__)

from .FloorPlan import views
from .JiShuBu import views
from .PlanDX import views
from .PlanDye import views
from .Service import views
