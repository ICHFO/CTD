import ibm_db
from app import get_db, ctdcfg


def get_resource_ids():
    ids = []
    sql = "select res_id from {}.res with ur".format(ctdcfg.schema)
    stmt = ibm_db.exec_immediate(get_db(), sql)
    result = ibm_db.fetch_assoc(stmt)
    while result:
        ids.append(result['RES_ID'])
        result = ibm_db.fetch_assoc(stmt)
    return ids


def get_resource_keys(res_id):
    resource_keys = []
    sql = "select key_naam, key_geldig, key_id from {0}.resm r, {0}.key k where r.resm_res_id = '{1}' and r.resm_key_id = k.key_id".format(ctdcfg.schema,
                                                                                                                                           res_id)
    stmt = ibm_db.exec_immediate(get_db(), sql)
    result = ibm_db.fetch_assoc(stmt)
    while result:
        resource_keys.append(result)
        result = ibm_db.fetch_assoc(stmt)
    return resource_keys


def update_resource_keys(mod_keys):
    print(mod_keys)
    for key in mod_keys:
        sql = "update {}.key set key_geldig = {} where key_id = {}".format(ctdcfg.schema, key['KEY_GELDIG'], key['KEY_ID'])
        print(sql)
        result_set = ibm_db.exec_immediate(get_db(), sql)


def get_five_best(res_id):
    vacancies = []
    sql = """select vac_url, sum(mapvr_vac_a_freq + mapvr_res_a_freq) as s 
             from {0}.mapvr, {0}.vac 
             where vac_id = mapvr_vac_id 
               and mapvr_res_id = '{1}'
             group by vac_url 
             order by s desc
             fetch first 5 rows only
             with ur
          """.format(ctdcfg.schema, str(res_id))
    stmt = ibm_db.exec_immediate(get_db(),sql)
    result = ibm_db.fetch_assoc(stmt)
    while result:
        vacancies.append(result)
        result = ibm_db.fetch_assoc(stmt)
    print(vacancies[0])
    return vacancies