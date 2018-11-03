import  logging, sys, os
from logging.handlers import RotatingFileHandler

def LogInit(environment):
    logger = logging.getLogger(environment+'.log')
    logger.setLevel(logging.DEBUG)

    fh = RotatingFileHandler(os.path.join(str(sys.path[0]),'log',environment + '.log'), 'a', 1000000, 3)

    fh.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    fh.setFormatter(formatter)

    logger.addHandler(fh)

def WriteIntoLogFile(line,message):

    logger = logging.getLogger(line + ".log")
    logger.debug(message)
