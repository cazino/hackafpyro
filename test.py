# -*- encoding: utf-8 -*-

import datetime
import requests
from bs4 import BeautifulSoup
import page


def get_afpyro():
    resdict = dict()
    res = requests.get('http://afpyro.afpy.org/')
    soup = BeautifulSoup(res.text)
    alist = soup.article.find_all('a')
    for link in alist:
        if link.get('class') is None:
            text = link.getText()
            href = link.get('href')
            clean_text = text.split('-')[0]
            date_str = href.split('/')[-1].split('.')[0]
            date_obj = datetime.datetime.strptime(date_str, "%Y_%m_%d").date()
            resdict[clean_text] = (date_obj, href)
    return resdict


from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    afpyro = get_afpyro()
    now = datetime.datetime.now()
    deltas = dict()
    for name, (dt, href) in afpyro.items():
        deltas[name] = (dt - now.date(), href)

    h2s = ""
    for name, (delta, href) in deltas.items():
        h2s += u"""<h2><a href="http://afpyro.afpy.org%s">%s dans %s jours</a></h2>""" % (href, name, delta.days)
    return page.page.format(h2s=h2s)


if __name__ == "__main__":
    app.run()
