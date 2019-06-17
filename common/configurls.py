from urllib3.util.url import Url
import common

class URLConfigs():
    def __init__(self, michost, gpshost, sahost):
        self.MIC_HOST = Url(scheme='http', host=michost, port=common.micport)
        self.GPS_HOST = Url(scheme='http', host=gpshost, port=common.gpsport)
        self.SA_HOST = Url(scheme='http', host=sahost, port=common.saport)