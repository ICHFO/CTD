import os


class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = 'uploads'
    
class DevConfig(Config):
    ctd_server = "192.168.1.246"
    ctd_database = "ctddev"
    ctd_port = 50010
    ctd_user = "db2dev"
    ctd_password = "db2dev"
    schema = "DEV"

class AccConfig(Config):
    ctd_server = "192.168.1.246"
    ctd_database = "ctdtst"
    ctd_port = 50030
    ctd_user = "db2tst"
    ctd_password = "db2tst"
    schema = "TST"
    
class PrdConfig(Config):
    ctd_server = "192.168.1.246"
    ctd_database = "ctdprd"
    ctd_port = 50020
    ctd_user = "db2prd"
    ctd_password = "db2prd"
    schema = "PRD"
    
config_switch={
    "DEV" : DevConfig,
    "ACC" : AccConfig,
    "PRD" : PrdConfig
}

def get_config(env):
    config = config_switch.get(env, "DEV")
    return config()
