import argparse
import io
import json
import lxml.etree
import pycurl
import wptools
import time
import urllib.parse

def wikipedia_fetch_prof(q, silent=True):
    langs = ["ja", "en"]

    # 日本人でも日本語版のinfoboxが（なぜか）取れない人がいるので
    for l in langs:
        # https://www.mediawiki.org/wiki/API:Parsing_wikitext/ja
        # 大いにwptoolsのソースを引用
        url = (f"https://{l}.wikipedia.org/w/api.php?"
               f"action=parse&page={urllib.parse.quote(q)}"
               "&prop=parsetree&format=json&formatversion=2&redirect")
        with io.BytesIO() as b:
            curl = pycurl.Curl()
            curl.setopt(pycurl.URL, url)
            curl.setopt(pycurl.WRITEFUNCTION, b.write)
            curl.perform()
            body = b.getvalue()
        data = json.loads(body)
        ptree = data.get("parse")
        if ptree:
            ptree = ptree.get("parsetree")

        if not ptree:
            continue

        # infobox らしいものを探す
        for item in lxml.etree.fromstring(ptree).\
                xpath("//template/part/value[translate("
                        f"normalize-space(text()),' ','')='{q}']/../.."):
            box = wptools.utils.template_to_dict(item)
            if box:
                return box

    # 最終的になんにもなかった場合は LookUpError を投げる
    # ページがない or Box がない
    raise LookupError

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("q")
    parser.add_argument("--silent", action="store_true")
    args = parser.parse_args()

    try:
        start = time.time()
        res = wikipedia_fetch_prof(args.q, silent=args.silent)
        end = time.time()
        print(res, "etime: ", end - start)
    except Exception as e:
        print(e)
