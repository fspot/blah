from flask import Flask, render_template
from utils import jsoncrossdomain, ser_handler, request
from database import db
import json

app = Flask(__name__)


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
    return request.form['site']


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


@app.route('/api/<site>/<article>/embed.js')
def embed_js(site, article):
    # penser au mimetype javascript
    return "alert('loul');"


if __name__ == "__main__":
    app.run(debug=True)
