import app.ctdcore.globalProperty as gp
import pdftotext
from app.ctdcore.log import LogInit, WriteIntoLogFile
from app.ctdcore.sqlStatement import res_exist, insert_res, delete_resm, select_key, insert_keyword, select_resm, update_resm, insert_resm, update_res,insert_ress, select_keywords
from datetime import datetime
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def init(args):

    if len (args) != 0 :
        environment = args[0]
        cv_file = args[1]

        config = gp.config()
        config.init_property(environment, cv_file)

        LogInit(gp.config.schema)


def check_keyword(keyword):
    new_keyword = keyword

    if keyword == u'\u2022':
        new_keyword = '.'

    if keyword == u'\u2713':
        new_keyword = 'v'

    if keyword == u'\u2013':
        new_keyword = '-'

    if keyword == u'\u2018' or keyword == u'\u2019':
        new_keyword = ''

    if "'" in keyword:
        new_keyword = ''

    #kevin stinkt

    return new_keyword

def add_from_pdf(environment, path_to_pdf):
    arg=[]
    arg.append(environment)
    arg.append(path_to_pdf)

    init(arg)

    #keywords, name, forename = read_pdf(path_to_pdf)
    #res, new_res = res_exist(forename, name)

    res = process_file(gp.config.cv_file)

    res_keywords = select_keywords(res)

    return res_keywords


def read_pdf(file):
    with open(file, "rb") as f:
        pdf = pdftotext.PDF(f)

    text = ""
    # Iterate over all the pages
    for page in pdf:
        text += page

    # The word_tokenize() function will break our text phrases into #individual words
    tokens = word_tokenize(text)

    #ix = tokens.index('Name')
    #name = tokens[ix+3]
    #forename = tokens[ix+2]
    name = str(file).split('.')[1]
    forename = str(file).split('.')[0]

    # we'll create a new list which contains punctuation we wish to clean
    punctuations = ['(', ')', ';', ':', '[', ']', ',']
    # We initialize the stopwords variable which is a list of words like #"The", "I", "and", etc. that don't hold much value as keywords
    stop_words = stopwords.words('english')
    # We create a list comprehension which only returns a list of words #that are NOT IN stop_words and NOT IN punctuations.
    keywords = [check_keyword(word.lower()) for word in tokens]

    #list_keywords  = list(set(keywords))   # without duplicates
    return keywords, name, forename


def process_keyword(keyword,res_id):

    #does this keyword exist ?
    extra_keyword=False

    key_id,key_valid,new_keyword = select_key(keyword)

    if new_keyword == True:
        insert_keyword(keyword)
        key_id, key_valid, new_keyword = select_key(keyword)

    #is it a valid keyword ?
    if key_valid > 0:

        resm_freq = select_resm(res_id,key_id)

        if resm_freq > 0:
            #update the keyword frequence
            resm_freq=resm_freq + 1
            update_resm(resm_freq,res_id,key_id)
            extra_keyword=False
        else:
            insert_resm(res_id,key_id,keyword)
            extra_keyword=True

        good_keyword=True
    else:
        good_keyword=False

    return new_keyword, good_keyword, extra_keyword




def process_file(file):
    nbr_good_keys = 0
    nbr_bad_keys = 0    # never used ?
    nbr_new_keys = 0
    ts_start = datetime.now()


    keywords, name, forename = read_pdf(file)

    res, new_res = res_exist(forename, name)

    if new_res:
        insert_res(res)

    delete_resm(res["res_id"])


    for current_word in keywords:
        new_keyword, good_keyword, extra_keyword = process_keyword(current_word, res["res_id"])

        if good_keyword:
            if extra_keyword:
                nbr_good_keys = nbr_good_keys+1
        else:
            nbr_bad_keys = nbr_bad_keys+1

        if new_keyword:
            nbr_new_keys=nbr_new_keys+1

    # Pas RES_D_SKILLSFIRST en aantal keywoorden (=goede+nieuwe) aan in RES
    update_res(res["res_id"], nbr_good_keys)


    #insert into RESS een rij voor de verwerking van dit profile met x keywoorden
    nbr_keywords = nbr_good_keys + nbr_new_keys

    insert_ress(ts_start,res["res_id"], nbr_keywords)

    return res['res_id']



def main(args):

    init(args)
    WriteIntoLogFile(gp.config.schema, "Main : IN    ---- V03")

    startTime=datetime.now()

    process_file(gp.config.cv_file)


    WriteIntoLogFile(gp.config.schema, "script duration: "+str(datetime.now()-startTime))
    WriteIntoLogFile(gp.config.schema, "Main : OUT")



if __name__== "__main__" :

    #main(sys.argv[1:])
    main(["DEV","/Users/admin/CTD/scripts/python/phase_2/opvullen_RESM/CV/CV PBR_Mei2018_Engels.pdf"])



#read_pdf gives back a dictionary

#{
# "":1,
# "":3
#}

