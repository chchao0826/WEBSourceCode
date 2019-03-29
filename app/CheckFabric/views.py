# -*-coding:utf-8-*-
from . import CheckFabric
from flask import render_template, Flask, request

import json

# 主页
@CheckFabric.route('/')
def index():
    return render_template('CheckFabric/CheckFabric.html')
