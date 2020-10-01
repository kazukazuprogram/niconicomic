#!/usr/bin/env python3
# coding: utf-8

from requests import Session
from bs4 import BeautifulSoup as bs
from argparse import ArgumentParser
from urllib.parse import urlparse
from re import compile
from time import sleep

max_retry = 3
global_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) "
                  "Gecko/20100101 Firefox/81.0"
}


def download(url, s, retry=0):
    if retry != 0:
        print("Retry({})".format(retry))
    try:
        g = s.get(url, headers=global_headers)
        g.raise_for_status()
    except Exception as e:
        print("Error: {}".format(e))
        if retry > max_retry:
            return
        print("Retry after 5 sec")
        sleep(5)
        return download(url=url, retry=retry + 1)
    f = bs(g.text, "lxml")
    thumb_url = f.select("img.thumb")[0].get("src")
    thumb_parse = urlparse(thumb_url)
    print(thumb_parse.path.split("/")[3])


def main(args, s=Session(), recursive=False):
    # FEATURE: ゲストユーザーで見るのがキツイので、ログインを実装する
    if args.test:
        url = "https://seiga.nicovideo.jp/watch/mg508644"
        download(url=url, s=s)
    for arg in args.url_or_code:
        code = compile("^mg[0-9]+$")
        m = code.match(arg)
        if m is not None:
            print(m.string)
        else:
            url = urlparse(arg)
            if ["seiga.nicovideo.jp", "nico.ms"] in url.netloc:
                print("URL is :", arg)
            else:
                print("\"{}\" is not valid URL.")


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('url_or_code', metavar='URL_or_code', nargs='*',
                        help='Webpage URL or code(mg******)')
    parser.add_argument('--test', "-t", action="store_true",
                        help='Test this program')
    args = parser.parse_args()
    if len(args.url_or_code) == 0 and not args.test:
        parser.print_help()
    else:
        main(args=args)
