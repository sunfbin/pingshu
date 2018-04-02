import sys, os, re, time, json

def get_chapter_name(num):
    if num < 10:
        return "000" + str(num)
    elif num < 100:
        return "00" + str(num)
    elif num < 1000:
        return "0" + str(num)
    else:
        return str(num)


# get first_num, dir_name from argv
def main(argv):
    if len(argv) < 2:
        print "param error"
        sys.exit(1)

    dir_name = argv[0]
    begin_num = int(argv[1])
    print "main: dir is %s and begin number is %i " % (dir_name, begin_num)

    for file_e in os.listdir(dir_name):
        if os.path.isfile(os.path.join(dir_name, file_e)):
            new_name = get_chapter_name(begin_num)
            new_name = new_name + dir_name + file_e
            os.rename(os.path.join(dir_name, file_e),os.path.join(dir_name, new_name))
            begin_num += 1
        

if __name__ == "__main__":
    main(sys.argv[1:])
