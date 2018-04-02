import sys, os, re, time, json


# get first_num, dir_name from argv
def main(argv):
    if len(argv) < 2:
        print "param error"
        sys.exit(1)

    dir_name = argv[0]
    begin_num = argv[1]
    begin_num = int(begin_num)
    print "main: dir is %s and begin number is %i " % (dir_name, begin_num)

    for file_e in os.listdir(dir_name):
        new_name = file_e[-7:]
        os.rename(os.path.join(dir_name, file_e),os.path.join(dir_name, new_name))
        

if __name__ == "__main__":
    main(sys.argv[1:])
