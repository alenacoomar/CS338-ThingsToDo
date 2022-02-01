from application import app
from common.libs.DateHelper import getCurrentTime
class UrlManager(object):
    @staticmethod
    def buildUrl(path):
        config_domain = app.config['DOMAIN']
        return "%s%s"%(config_domain['www'], path)
    @staticmethod
    def buildStaticUrl(path):
        path = "/static" + path
        return UrlManager.buildUrl(path)
    @staticmethod
    def getReleaseVersion():
        ver = "%s"%(getCurrentTime("%Y%m%d%H%M%S%f"))
        release_path = app.config.get('RELEASE_PATH')
        return ver
