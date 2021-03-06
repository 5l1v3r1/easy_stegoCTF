#!/usr/bin/python
import sys, os, getopt

from modules import Exif_module, Strings_module, Stego_module, LSB_module, Binwalk_module


def main(argv):
    hlp = "-f <inputfile> -o <outputdirectory> [-s <String_to_search> [-g/--stego] [-m/--metadata] [-b/--binwalk] [-l/--lsb] [-t/--strings] [-x/--hexdump] [-e/--entropy] [-n/--noprint] [-r/--min-len <min_len_of_strings>]]"
    try:
        opts, args = getopt.getopt(argv,"hf:o:s:gmbltxenr:z",["help","ifile=","odir=","search=","stego","metadata","binwalk","lsb","strings","hexdump","entropy","noprint","min-len=","sanitize"])
    except getopt.GetoptError, err:
        print "~ %s" % str(err)
        print hlp
        sys.exit(2)

    general_urls = []
    stego_tools = []
    search, out_dir, min_len = "", "", 5
    try_all, print_each, try_stego, try_exif, try_binwalk, try_lsb, try_strings, try_hexdump, try_entropy, sanitize = True, True, False, False, False, False, False, False, False, False

    for opt, arg in opts:
        if opt == '-h':
            print hlp
            sys.exit(3)

        elif opt in ("-f", "--ifile"):
            inputfile = arg
            filename = inputfile.split("/")[-1]
            if (not os.path.isfile(inputfile)):
                print "Not a file: "+filename
                sys.exit(-1)

        elif opt in ("-o","--odir"):
            out_dir = arg
            if not os.path.exists(out_dir):
                try: 
                    os.makedirs(out_dir)
                except:
                    print "Not a directory or not enough permissions: "+out_dir
                    sys.exit(-2)
            if not os.path.isdir(out_dir) or not os.access(out_dir, os.W_OK):
                print "Not a directory or not enough permissions: "+out_dir
                sys.exit(-2)

        elif opt in ("-g","--stego"):
            try_all = False
            try_stego = True

        elif opt in ("-m","--metadata"):
            try_all = False
            try_exif = True

        elif opt in ("-b","--binwalk"):
            try_all = False
            try_binwalk = True

        elif opt in ("-l","--lsb"):
            try_all = False
            try_lsb = True

        elif opt in ("-t","--strings"):
            try_all = False
            try_strings = True
        
        elif opt in ("-x","--hexdump"):
            try_hexdump = True
	    try_all= False

        elif opt in ("-e","--entropy"):
            try_all = False
            try_entropy = True

        elif opt in ("-s", "--search"):
            search = arg
        
        elif opt in ("-n", "--noprint"):
            print_each = False

        elif opt in ("-r","--min-len"):
            if arg.isdigit():
                min_len = int(arg)

        elif opt in ("-z", "--sanitize"):
            sanitize = True

    if not out_dir or not inputfile:
        print "No out directory"
        print hlp    
        sys.exit()


    print "File input: "+filename+"\n"


    # Binwalk MODULE
    bwlk = Binwalk_module(inputfile, out_dir, try_hexdump, search, sanitize)
    if (try_binwalk):
        bwlk.execute()

    # Exif MODULE
    exif = Exif_module(inputfile, search)
    if (try_exif):
        exif.execute()

    # Strings MODULE
    strings = Strings_module(inputfile, search, min_len)
    if (try_strings):
        strings.execute()

    # Stego MODULE
    stego = Stego_module(inputfile, out_dir, search, min_len, try_all, try_stego, try_hexdump, try_entropy)
    if (try_all or try_stego or try_hexdump or try_entropy):
        stego.execute()

    # LSB MODULE
    lsb = LSB_module(inputfile, out_dir, search, min_len)
    if (try_all or try_lsb):
        lsb.execute()



    ######## Print output #########
    print "###### General Usefull URLs ######"
    for url in general_urls:
        print url
    for tool in stego_tools:
        print tool
    print "###### End URLs ######\n"

    #Search MODULE
    if search != "":
        print "###### Search ######"
        if bwlk.get_found():
            print "!/\!/\!/\!/\!/\!/\! SEARCH FOUND IN BINWALK"
            bwlk.print_found()
        
        if exif.get_found():
            print "!/\!/\!/\!/\!/\!/\! SEARCH FOUND IN EXIF"
            exif.print_found()

        if exif.get_found():
            print "!/\!/\!/\!/\!/\!/\! SEARCH FOUND IN STRINGS"
            strings.print_found()

        if stego.get_found():
            print "!/\!/\!/\!/\!/\!/\! SEARCH FOUND IN STEGO"
            stego.print_found()

        if lsb.get_found():
            print "!/\!/\!/\!/\!/\!/\! SEARCH FOUND IN LSB"
            lsb.print_found()

        print "###### End Search ######"
        print


    if print_each:
        bwlk.mprint()
        exif.mprint()
        strings.mprint()
        stego.mprint()
        lsb.mprint()


if __name__ == "__main__":
   main(sys.argv[1:])
