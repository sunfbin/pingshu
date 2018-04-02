import sys, os, re, time, json
from subprocess import call


# init book-url map
books = None
try:
    file_b = open("pingshu_list.json")
    books = json.loads(file_b.read())
    file_b.close()
    print books
except Exception as e:
    print e
    sys.exit(1)


def get_book_info(book_name):
    # get the top url and total chapter number by book name
    url = None
    total = 0
    try:
        url = books[book_name]["url"]
        total = books[book_name]["total"]
        print "get_book_url: url for " + book_name + " is " + url
    except:
        print "get_book_url:Fail to get url: " + book_name + " not exist"
        sys.exit(1)
    return url, total


def get_chapter_url(chapter, book_url):
    if chapter == 1:
        return book_url;
    else:
        return book_url + str(chapter) + ".html"


def get_download_url(url, chap_num):
    command_str = "wget " + url
    status = call(command_str, shell=True)
    if status < 0:
        print ("failed to get chapter content: " + url)
        sys.exit(1)
    else:
        index_file_name = str(chap_num) + ".html"
        if chap_num == 1:
            index_file_name = "index.html"

        file_html = open(index_file_name, "r")
        result = None
        temp_name = None
        for line in file_html:
            if re.search("href=.*mp3", line):
                result = line
                break

        if result is not None:
            begin_idx = result.index("http")
            end_idx = result.index(".mp3") + 4
            result = result[begin_idx:end_idx]
            n_idx = result.rfind("/") + 1
            temp_name = result[n_idx:]
            print "get_download_url: download url is " + result
            print "get_download_url: temporary file name is " + temp_name

        # clean up temp files
        file_html.close()
        command_str = "rm " + index_file_name
        call(command_str, shell=True)
        return result, temp_name

def get_chapter_name(num):
    suffix = ".mp3"
    if num < 10:
        return "00" + str(num) + suffix
    elif num < 100:
        return "0" + str(num) + suffix
    elif num < 1000:
        return str(num) + suffix


def check_chapter_status(chap_name, book_name):
    path_str = book_name
    if os.path.exists(path_str):
        chap_file = book_name + "/" + chap_name
        return os.path.exists(chap_file)
    else:
        command_str = "mkdir -p ./%s" % book_name
        print "check_chapter_status: create book directory: " + command_str
        status = call(command_str, shell=True)
        if status < 0:
            print ("failed to create directory for book" + book_name)
            sys.exit(1)


def download_chapters(url, total_chaps, book_name):
    for num in range(1, total_chaps+1):
        chap_name = get_chapter_name(num)
        chap_exist = check_chapter_status(chap_name, book_name)
        if not chap_exist:
            c_url = get_chapter_url(num, url)

            # get the html first and grep the download url from it
            d_url, temp_name = get_download_url(c_url, num)
            if d_url is None:
                print "download_chapters:Fail to get accurate download url for " + c_url
                sys.exit(1)

            
            # download file and rename it
            command_str = "wget " + d_url
            status = call(command_str, shell=True)
            command_str = "mv " + temp_name + " " + book_name + "/" + chap_name 
            status = call(command_str, shell=True)

            # sleep 2 seconds to rest
            time.sleep(2) 

def main(argv):
    if books is None:
        print "fail to get all book list. "
        sys.exit(1)

    if len(argv) < 1:
        print "please provide book name as parameter"
        sys.exit(1)

    book_name = argv[0]
    print "main: book_name is " + book_name

    url,total_chaps = get_book_info(book_name);
    print "main: total chapters number is " + str(total_chaps)

    download_chapters(url, total_chaps, book_name)


if __name__ == "__main__":
    main(sys.argv[1:])
