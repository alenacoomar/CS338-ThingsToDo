from application import app
from flask import request,g
from common.models.user import *
from common.libs.UserService import UserService
@app.before_request
def before_request():
    app.logger.info("----------------------")
    user_info =checkLogin()
    app.logger.info(user_info)
    g.current_user =None
    if user_info:
        g.current_user = user_info
    return

@app.after_request
def after_request(res):
    app.logger.info("---------after--------")
    return res

def checkLogin():
    cookies = request.cookies
    cookie_name = app.config['AUTH_COOKIE_NAME']
    auth_cookie = cookies[cookie_name] if cookie_name in cookies else None
    if auth_cookie is None:
        return False
    auth_info = auth_cookie.split("#")
    if len(auth_info) != 2:
        return False
    try:
        user_info = User.query.filter_by(id = auth_info[1]).first()

    except Exception:
        return False
    if user_info is None:
        return False
    if auth_info[0] != UserService.generateAuthCode(user_info):
        return False
    return user_info