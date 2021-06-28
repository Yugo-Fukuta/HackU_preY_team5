# coding: utf-8
import urllib.request as req
import urllib.parse as up
import lxml.html as lh
import re
import pprint
import json

#def wiki_search(query):
try:
    values = 'イチロー'
    s_url = 'https://ja.wikipedia.org/api/rest_v1/page/summary/' + up.quote(values)
    request = req.Request(url=s_url)
    res = req.urlopen(request, timeout=10).read()
    root = lh.fromstring(res.decode('utf-8'))
    apple = json.loads(res.decode('utf-8'))
    print(apple["extract"], apple["thumbnail"]["source"])
except:
    pass