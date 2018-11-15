from app import get_db
from app.ctdcore.log import WriteIntoLogFile
from app.ctdcore.globalProperty import config
import ibm_db


class sqlConnection(object):

    def get_ctd_connection(self):
        return get_db()

    def log_sql_query(self,stmt, result):
            WriteIntoLogFile(config.schema, "\n    " + stmt.strip())
            if ibm_db.num_rows(result) != -1:
                WriteIntoLogFile(config.schema, "rows affected: {}".format(ibm_db.num_rows(result)))


