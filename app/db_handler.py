import ibm_db
from app import get_db


def get_resource_ids():
    ids = []
    sql = "select res_id from dev.res with ur"
    stmt = ibm_db.exec_immediate(get_db(), sql)
    result = ibm_db.fetch_assoc(stmt)
    while result:
        ids.append(result['RES_ID'])
        result = ibm_db.fetch_assoc(stmt)
    return ids


def get_resource_keys(res_id):
    resource_keys = []
    sql = "select key_naam, key_geldig, key_id from dev.resm r, dev.key k where r.resm_res_id = '{}' and r.resm_key_id = k.key_id".format(res_id)
    stmt = ibm_db.exec_immediate(get_db(), sql)
    result = ibm_db.fetch_assoc(stmt)
    while result:
        resource_keys.append(result)
        result = ibm_db.fetch_assoc(stmt)
    return resource_keys


def update_resource_keys(mod_keys):
    print(mod_keys)
    for key in mod_keys:
        sql = "update dev.key set key_geldig = {} where key_id = {}".format(key['KEY_GELDIG'], key['KEY_ID'])
        print(sql)
        result_set = ibm_db.exec_immediate(get_db(), sql)
