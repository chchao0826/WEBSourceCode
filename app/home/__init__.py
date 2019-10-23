# coding:utf8

from flask import Blueprint

Home = Blueprint('Home',__name__)

from . import views
