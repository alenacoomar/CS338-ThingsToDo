from application import app
from controllers.index import index_page

from flask_debugtoolbar import DebugToolbarExtension
toolbar = DebugToolbarExtension(app)

from interceptors.Auth import *
from interceptors.errorHandler import *
from controllers.member import *

app.register_blueprint( index_page,url_prefix = "/" )
app.register_blueprint(member_page, url_prefix = "/member")

from common.libs.UrlManager import UrlManager
app.add_template_global(UrlManager.buildStaticUrl,'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl,'buildUrl')