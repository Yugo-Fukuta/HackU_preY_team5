import argparse
import wptools


def wikipedia_fetch_prof(q, silent=True):
    langs = ["ja", "en"]
    infobox = None

    # 日本人でも日本語版のinfoboxが（なぜか）取れない人がいるので
    for l in langs:
        try:
            so = wptools.page(q, lang=l, silent=silent).get_parse()
        except LookupError as e:
            continue

        infobox = so.data["infobox"]
        if infobox:
            break

    # infobox が取れなかったらとりあえず LookUpError を投げる
    if infobox:
        return infobox
    else:
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
