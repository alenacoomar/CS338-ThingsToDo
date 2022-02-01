from flask import Flask, Blueprint, request, make_response, jsonify, render_template
from application import db
from common.models.user import User
from common.libs.Helper import *
index_page = Blueprint("index_page", __name__)

@index_page.route("/")
def template():
    name = "chenyu"
    context = {"name": name}
    context['user'] = {"nickname": "tommy", "qq": "xxxx", "homepage": "http://www.qq.com"}
    context['num_list'] = [1, 2, 3, 4, 5]

    result = User.query.all()
    context['result'] = result
    return ops_render("index.html", context)
