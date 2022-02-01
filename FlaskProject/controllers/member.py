from application import app,db
from flask import Blueprint,render_template,request,jsonify,session,make_response,redirect
from common.libs.Helper import *
from common.models.user import User
from common.libs.UserService import *
from common.libs.DateHelper import *
from common.libs.UrlManager import *
member_page = Blueprint("login_page",__name__)

@member_page.route("/signup",methods=["GET","POST"])
def signup():
    if request.method == "GET":
        return render_template("member/signup.html")
    else:
        req = request.values
        login_name = req['login_name'] if "login_name" in req else ""
        login_pwd1 = req['login_pwd1'] if "login_pwd1" in req else ""
        login_pwd2 = req['login_pwd2'] if "login_pwd2" in req else ""
        if login_name is None or len(login_name) < 1:
            return ops_renderErrJSON(msg="username is not correct")
        if login_pwd1 is None or len(login_pwd1) < 8:
            return ops_renderErrJSON(msg="password not ok")
        if login_pwd2 != login_pwd1:
            return ops_renderErrJSON(msg ="password not identical")
        print("helloworld")
        user_info = User.query.filter_by(login_name=login_name).first()
        if user_info:
            return ops_renderErrJSON(msg="User already exist")
        model_user = User()
        model_user.login_name = login_name
        model_user.nickname = login_name
        model_user.login_salt = UserService.geneSalt(8)
        model_user.login_pwd = UserService.genePwd(login_pwd1, model_user.login_salt)
        print(model_user.login_pwd)
        print(model_user.login_salt)
        model_user.created_time = model_user.updated_time = getCurrentTime()
        db.session.add(model_user)
        db.session.commit()
        db.session.close()
        return ops_renderJSON(msg="Successfully signup")

@member_page.route("/login",methods = ["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("member/login.html")
    else:
        req = request.values
        login_name = req['login_name'] if "login_name" in req else ""
        login_pwd = req['login_pwd'] if "login_pwd" in req else ""
        if login_name is None or len(login_name) < 1:
            return ops_renderErrJSON(msg="The username is not correct")
        if login_pwd is None or len(login_pwd) < 8:
            return ops_renderErrJSON(msg="The password is not correct")
        user_info = User.query.filter_by(login_name=login_name).first()
        print(login_name)
        print(user_info)
        if user_info is None:
            print("hello world")
            return ops_renderErrJSON(msg="The username or the password is not correct")
        if user_info.login_pwd != UserService.genePwd(login_pwd, user_info.login_salt):
            print("this world")
            return ops_renderErrJSON(msg="The username or the password is not correct")
        if user_info.status != 1:
            print("you")
            return ops_renderErrJSON(msg="The account is banned")
        response = make_response(ops_renderJSON(msg="login successfully"))
        response.set_cookie(app.config['AUTH_COOKIE_NAME'],
                            "%s#%s"%(UserService.generateAuthCode(user_info),user_info.id), 60 *60 * 24)

        return response

@member_page.route("/logout")
def logout():
    response =make_response(redirect(UrlManager.buildUrl("/")))
    response.delete_cookie(app.config['AUTH_COOKIE_NAME'])
    return response
@member_page.route("/team")
def team():
    name = "chenyu"
    context = {"name": name}
    return ops_render("member/team.html", context)

@member_page.route("/transcript")
def transcript():
    name = "chenyu"
    context = {"name": name}
    return ops_render("member/transcript.html", context)
