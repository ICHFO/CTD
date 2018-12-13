import ibm_db
from app import get_db, ctdcfg as config
from datetime import date, datetime


def exec_stmt(stmt):
    result = ibm_db.exec_immediate(get_db(), stmt)
    # log_query(stmt, result)
    return result


def fetch_all(stmt):
    result = exec_stmt(stmt)
    record = ibm_db.fetch_both(result)
    output = list()
    while record:
        output.append(record)
        record = ibm_db.fetch_assoc(result)
    return output


def fetch_single(sql):
    record = exec_stmt(sql)
    return ibm_db.fetch_assoc(record)


def select_keywords(res_id):
    res = list()
    stmt = f"""
            select r.resm_res_id
                 , r.resm_key_naam
                 , r.resm_key_id
                 , k.key_geldig
            from {config.schema}.resm r
            left join {config.schema}.key on r.resm_key_id = k.key_id
            where r.resm_res_id = '{res_id}'"""

    for record in fetch_all(stmt):
        res_fetch = dict(res_id=str(record[0]),
                         key_naam=str(record[1]),
                         key_id=record[2],
                         key_geldig=record[3])
        res.append(res_fetch)

    return res


def resource_exists(resource_name):
    pass


def get_resource(resource_id):
    sql = f"select id, abbrev, fname, name, is_working from ctd.resource where id = {resource_id}"
    record = fetch_single(sql)
    return record


def insert_resource(resource):
    sql = f"insert into ctd.resource ( abbrev, fname, name, is_working )" \
          f"values ('{resource.abbrev}', '{resource.fname}', '{resource.name}', {resource.is_working})"


def delete_resource(resource_id):
    pass


def update_resource(resource):
    pass


def get_resource_map(resoure_id):
    resource_map = dict()
    sql = f"select resource_id, vacancy_id, matching_keys, pct_resource, pct_vacancy " \
          f"from ctd.resource_vacancy_map " \
          f"where resource_id = {resource_id}"
    record = ibm_db.fetch_assoc(sql)
    if record:
        resource_map.update(id=record['ID'], name=record['NAME'])
        record = ibm_db.fetch_assoc(sql)
    return resource_map


def insert_resource_map(resource_map):
    sql = f"insert into ctd.resource_vacancy_map" \
          f"values ({resource_map.resource_id}, {resource_map.vacancy_id}" \
          f"       ,{resource_map.matching_keys}, {resource_map.pct_resource}," \
          f"       ,{resource_map.pct_vacancy})"
    exec_stmt(sql)

def update_resource_map(resource_map):
    sql = f"update ctd.resource_vacancy_map" \
          f"set matching_keys = {resource_map.matching_keys}" \
          f"  , pct_resrour"

def delete_resource_map(resource_id):
    stmt = f"delete from ctd.resource_vacancy_map where resource_id = '{resource_id}'"
    exec_stmt(stmt)


def key_exists(key_name):
    pass

def select_key(keyword):
    stmt = f"select key_id, key_geldig from {config.schema}.key where key_naam = '{str(keyword)}'"
    record = fetch_single(stmt)

    if record:
        new_key = False
        key_id = record[0]
        key_valid = record[1]
    else:
        new_key = True
        key_id = key_valid = ""

    return (key_id, key_valid, new_key)


def insert_key(keyword):
    # key_geldig = 9 -> to be checked
    stmt = """insert into {0}.key (key_naam, key_geldig) values ('{1}', 9)
		   """.format(config.schema, str(keyword))
    exec_stmt(stmt)


def select_resm(res_id, key_id):
    stmt = """select resm_a_freq
			  from {0}.resm
			  where resm_res_id = '{1}'
			    and resm_key_id = {2}
		   """.format(config.schema, res_id, str(key_id))
    record = fetch_single(stmt)

    if record:
        resm_freq = record[0]
    else:
        resm_freq = 0

    return resm_freq


def update_resm(resm_freq, res_id, key_id):
    stmt = """update {0}.resm 
			  set resm_a_freq = {1}
			  where resm_res_id = '{2}'
			    and resm_key_id = {3}
		   """.format(config.schema, str(resm_freq), res_id, str(key_id))
    exec_stmt(stmt)


def insert_resm(res_id, key_id, keyword):
    # maxversie, geldig, frequentie + gewicht + niveau
    stmt = """insert into {0}.resm values ('{1}', {2}, 1, 1, 1, 0, 0, '{3}')
		   """.format(config.schema, res_id, str(key_id), str(keyword))
    exec_stmt(stmt)


def update_res(res_id, nbr_good_keys):
    # Pas VAC_D_SKILLSFIRST en aantal keywoorden (=goede+nieuwe) aan in VAC
    stmt = """update {0}.res set res_a_freq = {1} where res_id = '{2}'
	       """.format(config.schema, str(nbr_good_keys), res_id)
    exec_stmt(stmt)


def insert_ress(ts_start, res_id, nbr_keywords):
    # statistieken van de verwerking van deze file opslaan in de VACS tabel
    # de som na de verwerking van alle files geeft de totaal bij de statistieke
    stmt = """insert into {0}.ress
			  (ress_ts_start, ress_ts_end, ress_res_id, ress_a_new)
			  values ('{1}', '{2}', '{3}', {4})
		   """.format(config.schema, str(ts_start), str(datetime.now()), res_id, str(nbr_keywords))
    exec_stmt(stmt)
