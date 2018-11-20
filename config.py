import os


class Config(object):
    DEBUG = True
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    UPLOAD_FOLDER = 'uploads'
    
class DevConfig(Config):
    ctd_server = 192.168.1.246
    ctd_database = "ctddev"
    ctd_port = 50010
    ctd_user = "db2dev"
    ctd_password = "SuadaSoft"
