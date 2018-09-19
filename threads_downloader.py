from math import ceil
import requests
from threading import Thread
import json
import time

urls_s = (
        "https://api.hh.ru/vacancies/26551396?host=hh.ru",
        "https://api.hh.ru/vacancies/26086083?host=hh.ru",
        "https://api.hh.ru/vacancies/26609184?host=hh.ru",
        "https://api.hh.ru/vacancies/26604519?host=hh.ru",
        "https://api.hh.ru/vacancies/24956317?host=hh.ru",
        "https://api.hh.ru/vacancies/26739587?host=hh.ru",
        "https://api.hh.ru/vacancies/26282306?host=hh.ru",
        "https://api.hh.ru/vacancies/26717726?host=hh.ru",
        "https://api.hh.ru/vacancies/26626404?host=hh.ru",
        "https://api.hh.ru/vacancies/25985849?host=hh.ru")

vacs = []


class DownloadThread(Thread):
    def __init__(self, urls, number, res):
        Thread.__init__(self)
        self.number = number
        self.urls = urls
        self.res = res

    def run(self):
        for url in self.urls:
            resp = requests.get(url)
            if resp.status_code == requests.codes.ok:
                self.res.append(json.loads(requests.get(url).text))
            else:
                print("Status code: " + str(resp.status_code))
                print(url)


def start_dl_threads(urls, th_num, res):
    """
    Функция для многопоточного скачивания данных

    :param urls: Список url для скачивания
    :param th_num: Число потоков
    :param res: Список результатов
    """
    threads = []
    n = ceil(len(urls) / th_num)
    for i in range(th_num):
        t = DownloadThread(urls[i * n: (i + 1) * n], i, res)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()


if __name__ == "__main__":
    th_n = 20
    start_dl_threads(urls_s, th_n, vacs)
    print(len(vacs))
