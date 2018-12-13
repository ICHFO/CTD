import pdftotext
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import app.ctdcore.sqlStatement as sql


def add_from_pdf(file):
	res = process_file(file)
	res_keys = sql.select_keywords(res)
	return res_keys

	
def process_file(file):
	bad_keys = new_keys = good_keys = 0
	
	ts_start = datetime.now()
	keywords, name, fname = read_pdf(file)
	
	res, new_res = sql.res_exist(fname, name)
	
	if new_res:
		sql.insert_res(res)
		
	sql.delete_resm(res.get('res_id'))
	
	for current_key in keywords:
		new_key, good_key, extra_key = process_keyword(current_key, res.get('res_id'))
		
		if good_key:
			if extra_key:
				good_keys += 1
		else:
			bad_keys += 1
		
		if new_key:
			new_keys += 1
	# pas RES_D_SKILLSFIRST en aantal keywoorden (=goede+nieuwe) aan in RES
	sql.update_res(res.get('res_id'), good_keys)
	# insert into RESS een rij voor de verwerking van dit profile met x keywoorden
	total_keys = good_keys + new_keys
	sql.insert_ress(datetime.now(), res.get('res_id'), total_keys)
	
	return res.get('res_id')
		
	
def read_pdf(file):
	# list of punctuation chars we want to ignore
	punctuations = ['(', ')', ';', ':', '[', ']', ',']
	# list of English stop words like: I, The, and, ...
	stop_words = stopwords.words('english')

	with open(file, "rb") as pdf_file: 
		pdf = pdftotext.PDF(pdf_file)
	
	text = ""
	for page in pdf: 
		text += page
		
	tokens = word_tokenize(text)
	
	# name and first name are coming from the file name
	fname = str(file).split('.')[0]
	name = str(file).split('.')[1]
	
	# create list of tokens that are not in stop words or punctuation lists
	keywords = [check_keyword(word.lower()) for word in tokens]
	
	return (keywords, fname, name)


def check_keyword(keyword):
	key_switch = {
		u'\u2022' : '.',
		u'\u2713' : 'v',
		u'\u2013' : '-',
		u'\u2018' : '',
		u'\u2019' : '',
		"'" : ''
	}
	# return values based on keyword, if not found return keyword by default
	return key_switch.get(keyword, keyword)
	
	
def process_keyword(keyword, res_id):
	extra_key = False
	key_id, ,key_valid, new_key = select_key(keyword)
	
	if new_key:
		insert_keyword(keyword)
		key_id, ,key_valid, new_key = select_key(keyword)
		
	if key_valid > 0:
		resm_freq = sql.select_resm(res_id, key_id)
		if resm_freq > 0:
			resm_freq += 1
			sql.update_resm(resm_freq, res_id, key_id)
			extra_key = False
		else:
			sql.insert_resm(res_id, key_id, keyword)
			extra_key = True
	else:
		good_key = False
		
	return (new_key, good_key, extra_key)
