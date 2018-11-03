from log import WriteIntoLogFile
from globalProperty import config
import ibm_db


class sqlConnection(object):

    def get_ctd_connection(self):

        conn = ibm_db.connect("database={0};HOSTNAME={1};port={2};UID={3};PWD={4};".format(config.ctd_database,
                                                                                           config.ctd_server,
                                                                                           config.ctd_port,
                                                                                           config.ctd_user,
                                                                                           config.ctd_password), "", "")

        return conn

    def log_sql_query(self,stmt, result):
            WriteIntoLogFile(config.schema, "\n    " + stmt.strip())
            if ibm_db.num_rows(result) <> -1:
                WriteIntoLogFile(config.schema, "rows affected: {}".format(ibm_db.num_rows(result)))


