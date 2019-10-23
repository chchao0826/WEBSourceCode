# -*- coding: utf-8 -*-
from . import Home
from flask import Flask, render_template, jsonify, request
import json


# 主页
@Home.route('/')
def index():
    return render_template('Home/Index.html')


