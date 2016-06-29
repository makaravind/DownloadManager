import requests
import threading
import datetime
from tqdm import tqdm

def CreateEmptyFile(name, size):
    file_name = name+".bin"
    fp = open(file_name, "wb")
    fp.write('\0' * size)
    fp.close()


def WriteToFile(file_name, start, content):
    file_name = file_name + ".bin"
    with open(file_name, "r+b") as fp:
        fp.seek(start)
        var = fp.tell()
        fp.write(content)


def Worker(start, end, url, filename):
    headers = {'Range': 'bytes=%d-%d' % (start, end)}
    r = requests.get(url, headers=headers, stream=True)
    WriteToFile(filename, start, r.content)


def Main():
    url = 'http://rohinibarla.github.io/heros/04MartinFowler.jpg'
    r = requests.head(url)
    file_name = r.headers['content-type'].split('/')[0] + str(datetime.date.today())
    file_size = r.headers['content-length']
    no_chunks = 4
    chunk = int(file_size) / no_chunks

    CreateEmptyFile(file_name, int(file_size))

    for i in range(no_chunks):
        start = chunk * i
        end = start + chunk
        # print start, end
        t = threading.Thread(target=Worker, kwargs={'start': start, 'end': end, 'url': url, 'filename': file_name})
        t.setDaemon(True)
        t.start()

    main_thread = threading.current_thread()
    for t in tqdm(threading.enumerate()):
        if t is main_thread:
            continue
        t.join()
    print 'downloading completed.. %s' % file_name

Main()