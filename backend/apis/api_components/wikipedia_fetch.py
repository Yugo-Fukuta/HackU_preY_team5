import argparse
import lxml.etree
import wptools


def wikipedia_fetch_prof(q, silent=True):
    langs = ["ja", "en"]
    infobox = None

    # 日本人でも日本語版のinfoboxが（なぜか）取れない人がいるので
    for l in langs:
        try:
            so = wptools.page(q, lang=l, boxterm="Infobox", silent=silent).get_parse()
        except LookupError as e:
            continue

        infobox = so.data["infobox"]
        if infobox:
            return infobox

        # infobox が取れなかったらそれっぽいものを探す
        for item in lxml.etree.fromstring(so.data["parsetree"]).xpath(f"//template/part/value[translate(normalize-space(text()),' ','')='{q}']/../.."):
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
        print(wikipedia_fetch_prof(args.q, silent=args.silent))
    except Exception as e:
        print(e)
