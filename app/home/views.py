# -*- coding: utf-8 -*-
from . import home
from flask import Flask, render_template, jsonify, request
import json


# 主页
@home.route('/')
def index():
    return render_template('home/index.html')


