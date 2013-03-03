from flask import Flask
from utils import jsoncrossdomain, ser_handler
from database import db
import json

app = Flask(__name__)


# ==========================
# ===     WEB SITE       ===
# ==========================

@app.route('/')
def index():
    return 'plop'


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


if __name__ == "__main__":
    app.run(debug=True)
