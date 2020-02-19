# coding:utf8

from flask import Blueprint

ERP = Blueprint('ERP',__name__)

from . import views
