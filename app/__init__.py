from flask import Flask, g
from config import Config
from flask_bootstrap import Bootstrap
import ibm_db

app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

VALID_KEYS_VALS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

def connect_db():
    return ibm_db.pconnect("DATABASE=ctddev;HOSTNAME=192.168.1.246;PORT=50010;UID=ctd;PWD=SuadaSoft","","")


def get_db():
    if not hasattr(g, 'ibm_db'):
        g.ibm_db = connect_db()
    return g.ibm_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'ibm_db'):
        ibm_db.close(g.ibm_db)


from app import routes
