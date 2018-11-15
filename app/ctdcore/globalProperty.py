import json
import os
import sys

class config(object):

    global ctd_server
    global ctd_database
    global ctd_port
    global ctd_user
    global ctd_password

    global schema
    global cv_file

    def init_property(self,environment,cv_file):
        # load database config

        file = os.path.join(str(sys.path[0]),"Config","%s" % ("conf_{0}.json".format(environment)))

        with open(file) as config_db_file:
            conf = json.load(config_db_file)

        config.ctd_server = conf['ctd_server']
        config.ctd_database = conf['ctd_database']
        config.ctd_port = conf['ctd_port']
        config.ctd_user = conf['ctd_user']
        config.ctd_password = conf['ctd_password']

        config.schema = environment
        config.cv_file = cv_file

