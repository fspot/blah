#!/usr/bin/env python
# -*- coding:utf-8 -*-

from flask import Flask, render_template, request  # , session, make_response
from utils import crossdomain, ser_handler
from database import db
import json

app = Flask(__name__)
app.secret_key = '\x85\xf6\xa6\xe0\xd9\x8f\x11\xa5\xee\r#\xfd\xddh\xdb\\0\xcb'


# ==========================
# ===       SITES        ===
# ==========================

def init_sites():
    return {s['nom']: s['_id'] for s in db.sites.find()}

app.sites = init_sites()


# ==========================
# ===     WEB SITE       ===
# ==========================

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/inscription', methods=['GET'])
def inscription_get():
    return render_template('inscription.html')


@app.route('/inscription', methods=['POST'])
def inscription_post():
    #  session['site'] = request.form['site']
    site = {
        'nom': request.form['site']
    }
    db.sites.save(site)
    app.sites[site['nom']] = site['_id']
    return str(site['_id']) + ' ' + repr(app.sites)


@app.route('/<site>/newarticle', methods=['GET'])
def newarticle_get(site):
    return render_template('inscription.html')


@app.route('/<site>/newarticle', methods=['POST'])
def newarticle_post(site):
    # pour l'instant un article n'a que ça:
    id_site = app.sites[site]
    article = {
        'site': id_site,
        'nom': request.form['site'],
        'comments': []
    }
    db.articles.save(article)
    return str(article['_id'])


# ==========================
# ===     JSON  API      ===
# ==========================

@app.route('/api/')
@crossdomain(origin='*', is_json=True)
def api_index():
    comz = [x for x in db.comments.find({'name': 'luc'})]
    msg = json.dumps(comz, indent=2, default=ser_handler)
    return msg


@app.route('/api/<site>/<article>/comments')
@crossdomain(origin='*', is_json=True)
def get_comments(site, article):
    id_site = app.sites[site]
    rep = db.articles.find_one(
        {'site': id_site, 'nom': article},
        {'comments': 1, '_id': 0}
    )
    msg = json.dumps(rep, default=ser_handler)
    return msg


@app.route('/api/<site>/<article>/post', methods=['GET', 'OPTIONS', 'POST'])
@crossdomain(origin='*', headers="Content-Type", is_json=True)
def post_comment(site, article):
    id_site = app.sites[site]
    comment = request.json['comment']  # || request.form['comment'] ?
    # checker des trucs vis a vis du comment ici
    db.articles.update(
        {'site': id_site, 'nom': article},
        {'$push': {'comments': comment}}
    )
    msg = json.dumps({'status': 'ok'}, default=ser_handler)
    return msg


@app.route('/api/<site>/<article>/embed.js')
@crossdomain(origin='*')
def embed_js(site, article):
    # penser au mimetype javascript
    comz = ['com1', 'com2']
    comz = json.dumps(comz, default=ser_handler)
    sitecookie = request.cookies.get('site')
    if sitecookie is not None:
        print "si l'article n'existe pas, le creer"
    else:
        # import ipdb; ipdb.set_trace()
        print "pas confiance"
    return render_template('embed.js', site=site, article=article, comz=comz)


if __name__ == "__main__":
    app.run(debug=True)
