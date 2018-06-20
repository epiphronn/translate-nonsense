#!/usr/bin/env python

import sys
import re
import random
import time

if (sys.version_info[0] < 3):
    import urllib2
    import urllib
    import HTMLParser
else:
    import html.parser
    import urllib.request
    import urllib.parse


USAGE = ("""
Usage: (Windows terminal)
$ py make_nonsense.py text num_times init_lang

text- the text you want to make nonsense
num_times- amount of times to run through the translator (more is more nonsense)
init_lang- the language of the input text, default to English

Example:
$ py make_nonsense.py "Hello, how are you today?" 7 en
> Good where are you today i'm going well
""")

agent = {'User-Agent':
"Mozilla/4.0 (\
compatible;\
MSIE 6.0;\
Windows NT 5.1;\
SV1;\
.NET CLR 1.1.4322;\
.NET CLR 2.0.50727;\
.NET CLR 3.0.04506.30\
)"}

lang_codes = ['af','sq','am','ar','hy','az','eu','be','bs','bg','ca','ceb',
              'zh-CN','zh-TW','co','hr','cs','da','nl','en','eo','et','fi','fr',
              'fy','gl','ka','de','el','gu','ht','ha','haw','iw','hi','hmn','hu',
              'is','ig','id','ga','it','ja','jw','kn','kk','km','ko','ku','ky','lo',
              'la','lv','lt','lb','mk','mg','ms','ml','mt','mi','mr','mn','my','ne',
              'no','ny','ps','fa','pl','pt','pa','ro','ru','sm','gd','sr','st','sn',
              'sd','si','sk','sl','so','es','su','sw','sv','tl','tg','ta','te','th',
              'tr','uk','ur','uz','vi','cy','xh','yi','yo','zu']


def unescape(text):
    if (sys.version_info[0] < 3):
        parser = HTMLParser.HTMLParser()
    else:
        parser = html.parser.HTMLParser()
    return (parser.unescape(text))


def translate(text, out_lang, in_lang):
    base_link = "http://translate.google.com/m?hl=%s&sl=%s&q=%s"
    if (sys.version_info[0] < 3):
        text = urllib.quote_plus(text)
        link = base_link % (out_lang, in_lang, text)
        request = urllib2.Request(link, headers=agent)
        raw_data = urllib2.urlopen(request).read()
    else:
        text = urllib.parse.quote(text)
        link = base_link % (out_lang, in_lang, text)
        request = urllib.request.Request(link, headers=agent)
        raw_data = urllib.request.urlopen(request).read()
    data = raw_data.decode("utf-8")
    expr = r'class="t0">(.*?)<'
    re_result = re.findall(expr, data)
    if (len(re_result) == 0):
        result = ""
    else:
        result = unescape(re_result[0])
    return (result)


def nonsense(text, init_lang, num_times):
    cur_lang = init_lang
    new_lang = ''
    for _ in range(int(num_times)):
        new_lang = random.choice(lang_codes)
        text = translate(text, new_lang, cur_lang)
        cur_lang = new_lang
    text = translate(text, init_lang, cur_lang)
    return (text)


def main():
    if (len(sys.argv) < 3):
        print(USAGE)
        return (1)
    text = sys.argv[1]
    times = sys.argv[2]
    if (len(sys.argv) > 3):
        if (sys.argv[3] in lang_codes):
            lang = sys.argv[3]
        else:
            print('ERROR: Unsupported/incorrect langauge code')
            return(1)
    else:
        lang = "auto"
    print(nonsense(text, lang, times))
    return (0)


if __name__ == '__main__':
    main()
