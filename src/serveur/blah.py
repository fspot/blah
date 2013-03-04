from flask import Flask, render_template, request, session
from utils import jsoncrossdomain, ser_handler
from database import db
import json

app = Flask(__name__)
app.secret_key = '\x85\xf6\xa6\xe0\xd9\x8f\x11\xa5\xee\r#\xfd\xddh\xdb\\0\xcb'


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
    session['site'] = request.form['site']
    return session['site']


# ==========================
# ===     JSON  API      ===
# ==========================

@app.route('/api/')
@jsoncrossdomain(origin='*')
def api_index():
    comz = [x for x in db.comments.find({'name': 'luc'})]
    msg = json.dumps(comz, indent=2, default=ser_handler)
    return msg


@app.route('/api/<site>/<article>/comments')
@jsoncrossdomain(origin='*')
def get_comments(site, article):
    rep = {
        'test?': 'yep.',
        'info': [site, article],
    }
    msg = json.dumps(rep, default=ser_handler)
    return msg


@app.route('/api/<site>/<article>/post', methods=['GET', 'OPTIONS', 'POST'])
@jsoncrossdomain(origin='*', headers="Content-Type")
def post_comment(site, article):
    comment = request.json['comment']  # || request.form['comment'] ?
    msg = json.dumps({'comment': comment}, default=ser_handler)
    return msg


@app.route('/api/<site>/<article>/embed.js')
def embed_js(site, article):
    # penser au mimetype javascript
    comz = ['com1', 'com2']
    comz = json.dumps(comz, default=ser_handler)
    if 'site' in session:
        print "si l'article n'existe pas, le creer"
    else:
        import pdb; pdb.set_trace()
        print "pas confiance"
    return render_template('embed.js', site=site, article=article, comz=comz)


if __name__ == "__main__":
    app.run(debug=True)
