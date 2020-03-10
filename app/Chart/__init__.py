# coding:utf8

from flask import Blueprint

Chart = Blueprint('Chart',__name__)

from . import views
