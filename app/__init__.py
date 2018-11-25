from flask import Flask, g
from config import Config, get_config
from flask_bootstrap import Bootstrap
import ibm_db
import os

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
ctdcfg = get_config(os.environ['CTDENV'])

VALID_KEYS_VALS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def connect_db():
    connstr = "DATABASE={};HOSTNAME={};PORT={};UID={};PWD={}".format(ctdcfg.get('ctd_database'),
                                                                     ctdcfg.get('ctd_server'),
                                                                     ctdcfg.get('ctd_port'))
    return ibm_db.pconnect("DATABASE={};HOSTNAME={};PORT={};UID={};PWD={}","","")


def get_db():
    if not hasattr(g, 'ibm_db'):
        g.ibm_db = connect_db()
    return g.ibm_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'ibm_db'):
        ibm_db.close(g.ibm_db)


from app import routes
