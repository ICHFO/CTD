import ibm_db
from app import get_db, config
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
		record = ibm_db.fetch_both(result)
	return output
	
	
def fetch_1(stmt):
	result = exec_stmt(stmt)
	record = ibm_db.fetch_both(result)
	return record
	
	
def select_keywords(res_id):
	res = list()
	stmt = """select r.resm_res_id, r.resm_key_naam , r.resm_key_id, k.key_geldig
			  from {0}.resm r
			  left join {0}.key on r.resm_key_id = k.key_id
			  where r.resm_res_id = '{1}'
		   """.format(config.schema, res_id)
		  
	for record in fetch_all(stmt):
		res_fetch = dict(res_id=str(record[0]),
						 key_naam=str(record[1]),
						 key_id=record[2],
						 key_geldig=record[3])
		res.append(res_fetch)
	
	return res
	
	
def res_exists(fname, name):
	stmt = "select * from {0}.res where res_naam = '{1} {2}'".format(config.schema, fname, name)
	record = fetch_1(stmt)
	
	if record:
		new_res = False
		res = dict(res_id=record[0],
				   res_naam=record[1],
				   res_type_id=record[2],
				   res_bed_id=record[3],
				   res_d_raw=record[4],
				   res_d_prof=record[5],
				   res_d_skills=record[6],
				   res_d_end=record[7],
				   res_a_key=record[8])
	else:
		new_res = True
		res_id = fname[0:1].upper() + name[0:2].upper()
		full_name = "{} {}".format(fname, name)
		stmt = "select * from {0}.res where res_id = '{1}'".format(config.schema, res_id)
		
		if fetch_1(stmt): # id already exists, come up with new one
			res_id = fname[0:2].upper() + name[0:1].upper()
		
		res = dict(res_id=res_id,
				   res_naam=full_name,
				   res_type_id=0,
				   res_bed_id=1,
				   res_d_raw=date.today(),
				   res_d_prof=date.today(),
				   res_d_skills=date.today(),
				   res_d_end=None,
				   res_a_key=0)
	
	return (res, new_res)
	
	
def insert_res(res):
	stmt = """insert into {0}.res values ('{1}','{2}', {3}, {4}, '{5}', '{6}', '{7}', '{7}', {8})
		   """.format(config.schema, res.get('res_id'), res.get('res_naam'), str(res.get('res_type_id')),
					  str(res.get('res_bed_id')), str(res.get('res_d_raw')), str(res.get('res_d_prof')),
				      str(res.get('res_d_skills')), str(res.get('res_a_key')))
	exec_stmt(stmt)
	
	
def delete_resm(res_id):
	stmt = """delete from {0}.resm where resm_res_id = '{1}'
		   """.format(config.schema, res_id)
	exec_stmt(stmt)
	

def select_key(keyword):
	stmt = """select key_id, key_geldig from {0}.key where key_naam = '{1}'
		   """.format(config.schema, str(keyword))
	record = fetch_1(stmt)
	
	if record:
		new_key = False
		key_id = record[0]
		key_valid = record[1]
	else:
		new_key = true
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
	record = fetch_1(stmt)
	
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
