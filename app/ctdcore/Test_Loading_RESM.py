import sys
import loading_RESM


def main(args):

    #loading_RESM.main(args)

    keywords, name, forename = loading_RESM.read_pdf(args[1])

    


if __name__== "__main__" :

    #main(sys.argv[1:])
    main(["DEV","/Users/admin/CTD/scripts/python/phase_2/opvullen_RESM/CV/CV PBR_Mei2018_Engels.pdf"])
