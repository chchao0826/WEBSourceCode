# -*-coding:utf-8-*-
from . import CheckData
from flask import render_template, Flask, request, jsonify
import json
import time


@CheckData.route('/CheckTest/')
# 主页
def index():
    return render_template('CheckData/CheckTest.html')

