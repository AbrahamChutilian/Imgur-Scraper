from genericpath import isfile
import string
import random
import os
import sys
import _thread
import httplib2
import time
from termcolor import colored
import shutil
from threading import Timer

if len(sys.argv) < 2:
    sys.exit("\033[37mUsage: python3 " + sys.argv[0] +
             " (Number of threads)" + sys.argv[1] + " (Desired size in MB) ")


THREAD_AMOUNT = int(sys.argv[1])
DESIRED_SIZE = int(sys.argv[2]) * 1048576
FOLDER_SIZE = 0
START = True
DIR_NAME = "pics"

INVALID_SIZES = [0, 503, 543, 5082, 4939, 4940,
                 4941, 12003, 5556, 5553, 6167, 6217, 6218, 6426, 8192]

if not os.path.isdir(DIR_NAME):
    os.makedirs(DIR_NAME)


def get_file_path(fileName):
    return os.path.join(os.path.abspath(DIR_NAME), fileName)


def scrape_pictures(thread, foldS, desiredS):
    while foldS < desiredS:
        url = 'http://i.imgur.com/'
        length = random.choice((5, 6))
        if length == 5:
            url += ''.join(random.choice(string.ascii_letters +
                           string.digits) for _ in range(5))
        else:
            url += ''.join(random.choice(string.ascii_letters +
                           string.digits) for _ in range(3))
            url += ''.join(random.choice(string.ascii_lowercase +
                           string.digits) for _ in range(3))
            url += '.jpg'

            filename = get_file_path(url.rsplit('/', 1)[-1])

            h = httplib2.Http('cache/.cache' + thread)
            response, content = h.request(url)
            out = open(filename, 'wb')
            out.write(content)
            out.close()

            file_size = os.path.getsize(filename)
            if file_size in INVALID_SIZES:
                os.remove(filename)
            else:
                print(colored("[+] Valid: " + url, 'green'))
                foldS = sum(os.path.getsize(get_file_path(f))
                            for f in os.listdir('pics') if os.path.isfile(get_file_path(f)))


def stopScript():
    foldS = sum(os.path.getsize(get_file_path(f))
                for f in os.listdir('pics') if os.path.isfile(get_file_path(f)))
    fileCount = len([name for name in os.listdir(
        'pics') if os.path.isfile(get_file_path(name))])

    if(foldS >= DESIRED_SIZE):
        print(colored("Successfully downloaded ", 'green') +
              colored(str(fileCount), 'red') + colored(' files!', 'green'))
        return False


def deleteCacheFolder():
    print("Deleting cache folder")
    shutil.rmtree("cache", ignore_errors=True)


timeOut = Timer(4, deleteCacheFolder)


for thread in range(1, THREAD_AMOUNT + 1):
    thread = str(thread)
    try:
        _thread.start_new_thread(
            scrape_pictures, (thread, FOLDER_SIZE, DESIRED_SIZE))
    except:
        print('Error starting thread ' + thread)
print('Successfully started ' + thread + ' threads.')

while START:
    time.sleep(1)
    START = stopScript() if stopScript() is False else True

if(START is False):
    timeOut.start()
