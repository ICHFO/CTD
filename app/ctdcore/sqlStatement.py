from app.ctdcore.sqlConnection import sqlConnection
from app.ctdcore.globalProperty import config
import ibm_db
from datetime import date, datetime

def sql_exec(stmt):

    myConn = sqlConnection()
    sqcCon = myConn.get_ctd_connection()
    result = ibm_db.exec_immediate(sqcCon, stmt)
    myConn.log_sql_query(stmt,result)
    ibm_db.close(sqcCon)

def sql_fecth_all(stmt):

    myConn = sqlConnection()
    sqcCon = myConn.get_ctd_connection()
    result = ibm_db.exec_immediate(sqcCon, stmt)
    fetch_result=ibm_db.fetch_both(result)

    output = []
    while fetch_result:
        output.append(fetch_result)
        fetch_result = ibm_db.fetch_both(result)

    myConn.log_sql_query(stmt, result)
    ibm_db.close(sqcCon)

    return output


def sql_fecth_1(stmt):
    myConn = sqlConnection()
    sqcCon = myConn.get_ctd_connection()
    result = ibm_db.exec_immediate(sqcCon, stmt)
    fetch_result = ibm_db.fetch_both(result)

    output = []

    if fetch_result:
        output.append(fetch_result)

    myConn.log_sql_query(stmt, result)
    ibm_db.close(sqcCon)

    return output

def select_keywords(res_id):
    res = []

    stmt = """\

    select r.RESM_RES_ID, r.resm_key_naam, r.resm_key_id, k.KEY_GELDIG 
    from {0}.RESM r left join {0}.KEY k on r.resm_key_id = k.key_id
    where r.RESM_RES_ID = '{1}' 

    """.format(config.schema, res_id)

    fetch_all = sql_fecth_all(stmt)

    i = 0
    while i < len(fetch_all):
        fetch_result = fetch_all[i]
        res_fetch = {}

        res_fetch['res_id'] = str(fetch_result[0])
        res_fetch['key_naam'] = str(fetch_result[1])
        res_fetch['key_id'] = fetch_result[2]
        res_fetch['key_geldig'] = fetch_result[3]

        res.append(res_fetch)
        i+=1


    return res



def res_exist(forename, name):

    res ={}

    stmt = """\

    select * from {0}.RES where RES_NAAM = '{1} {2}'
    
    """.format(config.schema, forename, name)

    row = sql_fecth_1(stmt)

    if row:
        new_res=False
        res["res_id"]=row[0][0]
        res["res_naam"] = row[0][1]
        res["res_type_id"]=row[0][2]
        res["res_bed_id"] = row[0][3]
        res["res_d_raw"]=row[0][4]
        res["res_d_prof"]=row[0][5]
        res["res_d_skills"] = row[0][6]
        res["res_d_end"]=row[0][7]
        res["res_a_key"]=row[0][8]
    else:
        new_res=True
        res_id = forename[0:1].upper() + name[0:2].upper()

        stmt = """\
                
        select * from {0}.RES where RES_ID = '{1}'
        
        """.format(config.schema, res_id)

        row = sql_fecth_1(stmt)

        if row:
            res_id = forename[0:2].upper() + name[0:1].upper()

        res["res_id"]=res_id
        res["res_naam"] = forename + " " + name
        res["res_type_id"]=0
        res["res_bed_id"] = 1
        res["res_d_raw"]=date.today()
        res["res_d_prof"]=date.today()
        res["res_d_skills"] = date.today()
        res["res_d_end"]= ""
        res["res_a_key"]=0


    return res, new_res


def insert_res(res):

    stmt = """\
    
    Insert into {0}.RES values ('{1}', '{2}', {3}, {4}, '{5}', '{6}', '{7}', '{7}', {8})
    
    """.format(config.schema,res["res_id"],res["res_naam"],str(res["res_type_id"]),str(res["res_bed_id"]),str(res["res_d_raw"]),
               str(res["res_d_prof"]),str(res["res_d_skills"]),str(res["res_a_key"]))

    sql_exec(stmt)


def delete_resm(res_id):

    stmt = """\
    
    Delete from {0}.RESM where RESM_RES_ID = '{1}'

    """.format(config.schema, res_id)

    sql_exec(stmt)


def select_key(keyword):

    stmt = """\
    
    select KEY_ID, KEY_GELDIG from {0}.KEY where KEY_NAAM = '{1}'
        
    """.format(config.schema,str(keyword))


    #  UnicodeEncodeError: 'ascii' codec can't encode character u'\u2022' in position 0: ordinal not in range(128)


    row = sql_fecth_1(stmt)

    if row:
        key_id=row[0][0]
        key_valid=row[0][1]
        new_keyword=False
    else:
        key_id=""
        key_valid=""
        new_keyword=True


    return key_id, key_valid,new_keyword


def insert_keyword(keyword):
    #insert in KEY with 9 (to be check)

    stmt = """\
    
    Insert into {0}.KEY (KEY_NAAM, KEY_GELDIG) values ('{1}', 9) 
    
    """.format(config.schema,str(keyword))

    sql_exec(stmt)


def select_resm(res_id,key_id):

    stmt = """\
    
    select RESM_A_FREQ from {0}.RESM where RESM_RES_ID = '{1}' 
    and RESM_KEY_ID = {2}
    
    """.format(config.schema,res_id,str(key_id))

    row = sql_fecth_1(stmt)

    if row:
        resm_freq = row[0][0]
    else:
        resm_freq = 0


    return resm_freq


def update_resm(resm_freq,res_id,key_id):

    stmt = """\

    Update {0}.RESM SET RESM_A_FREQ = {1} 
    where RESM_RES_ID = '{2}'
    and RESM_KEY_ID = {3}
    
    """.format(config.schema,str(resm_freq),res_id,str(key_id))

    sql_exec(stmt)

def insert_resm(res_id,key_id,keyword):
    # maxversie, geldig, frequentie + gewicht + niveau

    stmt = """\
    
    Insert into {0}.RESM values ('{1}', {2},1,1,1,0,0,'{3}')  
    
    """.format(config.schema,res_id,str(key_id),str(keyword))

    sql_exec(stmt)


def update_res(res_id, nbr_good_keys):
    # Pas VAC_D_SKILLSFIRST en aantal keywoorden (=goede+nieuwe) aan in VAC

    stmt = """\
    
    Update {0}.RES set RES_A_FREQ = {1} 
    where RES_ID = '{2}'
    
    """.format(config.schema,str(nbr_good_keys),res_id)

    sql_exec(stmt)


def insert_ress(ts_start, res_id, nbr_keywords):
    # statistieken van de verwerking van deze file opslaan in de VACS tabel
    # de som na de verwerking van alle files geeft de totaal bij de statistieken

    stmt = """\
    
    insert into {0}.RESS (RESS_TS_START, RESS_TS_END, RESS_RES_ID, RESS_A_NEW) 
    values ('{1}', '{2}', '{3}', {4})
    
    """.format(config.schema,str(ts_start),str(datetime.now()),res_id,str(nbr_keywords))

    sql_exec(stmt)

