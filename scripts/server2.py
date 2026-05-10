from flask import Flask, render_template, request, abort, redirect, make_response, g, jsonify
import binascii
import hashlib
import sqlite3
import json

app = Flask(__name__)
app.secret_key = b'312edc37ea3f3f8d80c4a2c9752ae367'
salt = b'no_google_for_you'
FLAG = open("flag.txt", 'r').read().strip()

def get_db():
  db = getattr(g, '_database', None)
  if db is None:
    db = g._database = sqlite3.connect('users.db')
  return db

@app.teardown_appcontext
def close_connection(exception):
  db = getattr(g, '_database', None)
  if db is not None:
    db.close()

checks = [lambda a, b: ord(a[i]) ^ ord(b[i]) for i in range(0, 128)] 
def safe_hash_cmp(a, b):
  if len(a) != 128 or len(b) != 128:
    return False
  return sum(check(a, b) for check in checks) == 0

def do_login(user, password, admin):
  cookie = {'user': user, 'password': password, 'admin': admin}
  cookie['digest'] = hashlib.sha512(app.secret_key + bytes(json.dumps(cookie, sort_keys=True), 'ascii')).hexdigest()
  resp = make_response(redirect('/'))
  resp.set_cookie('auth', binascii.hexlify(json.dumps(cookie).encode('ascii')))
  return resp

def load_cookie():
  cookie = {}
  auth = request.cookies.get('auth')
  if auth:
    try:
      cookie = json.loads(binascii.unhexlify(auth).decode('ascii'))
      digest = cookie.pop('digest')
      if not safe_hash_cmp(digest, hashlib.sha512(app.secret_key + bytes(json.dumps(cookie, sort_keys=True), 'ascii')).hexdigest()):
        return False, {}
      # Check that the session is still valid
      result = get_db().cursor().execute("SELECT name FROM users WHERE name=? and password=?;", (cookie['user'], hashlib.sha512(salt + bytes(cookie['password'], 'ascii')).hexdigest())).fetchone()
      if result is None:
        return False, {}
    except:
      return False, {}
  return True, cookie

@app.route('/')
def index():
  ok, cookie = load_cookie()
  if not ok:
    return abort(403)
  return render_template('index.html', user=cookie.get('user', None), admin=cookie.get('admin', None), flag=FLAG)

@app.route('/login', methods=['POST'])
def login():
  user = request.form.get('user', '')
  password = request.form.get('password', '')
  if len(user) > 120:
    abort(400)
  c = get_db().cursor()
  result = c.execute("SELECT name, password, admin FROM users WHERE name ='%s';" % user).fetchone()
  if result is None:
    return abort(403)
  if user != result[0] or hashlib.sha512(salt + bytes(password, 'ascii')).hexdigest() != result[1]:
    response = jsonify({'error': "You're not %s!" % result[0]})
    response.status_code = 403
    return response
  return do_login(user, password, result[2])

@app.route('/logout', methods=['GET'])
def logout():
  resp = make_response(redirect('/'))
  resp.set_cookie('auth', '', expires=0)
  return resp

if __name__ == '__main__':
  app.run(debug=True, host="0.0.0.0", port=1337)
