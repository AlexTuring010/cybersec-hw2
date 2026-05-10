from flask import Flask, request, redirect, make_response
import sqlite3
import json
import time
import os
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)
app.secret_key = b'secretkey'  # We dont know which secret they using
DB_FILE = 'db.sqlite3'

# --- Utility functions ---

def get_db():
    db = sqlite3.connect(DB_FILE)
    db.row_factory = sqlite3.Row
    return db

# Strongly believe they use itsdangerous for token creation and verification
serializer = URLSafeTimedSerializer(app.secret_key)

def create_token(payload: dict) -> str:
    """Create a signed token using itsdangerous."""
    return serializer.dumps(payload)

def verify_token(token: str) -> dict | None:
    """Verify a signed token using itsdangerous."""
    try:
        return serializer.loads(token, max_age=3600)  # Tokens expire after 1 hour
    except Exception:
        return None

def generate_csrf_token():
    """Generate a signed CSRF token."""
    return serializer.dumps({'csrf': os.urandom(16).hex(), 'timestamp': time.time()})

def validate_csrf_token(csrf_token):
    """Validate the signed CSRF token."""
    try:
        data = serializer.loads(csrf_token, max_age=600)  # Token expires after 10 minutes
        return True
    except Exception:
        return False

def no_hacking_allowed(user_info=None):
    """Return a hacking warning message."""
    if user_info and 'user' in user_info:
        return f"""<html><head></head><body><h1 style="color:red">HEY, {user_info['user']}! STOP TRYING TO HACK US! WE KNOW WHO YOU ARE!!!!</h1></body></html>"""
    return """<html><head></head><body><h1 style="color:red">NO HACKING ALLOWED!!</h1></body></html>"""

# --- Routes ---

@app.route('/')
def index():
    token = request.cookies.get('auth')
    user_info = verify_token(token)

    # If the cookie does not exist or is invalid, create a new one with tick = 1
    if not user_info:
        user_info = {'tick': 1}
        token = create_token(user_info)

    csrf_token = generate_csrf_token()

    if 'user' not in user_info:
        resp = make_response(f"""
        <html><head>
        <title>The Face Book</title>
        <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
        <script type="text/javascript">
        $(document).ready(function() {{
          $('.facebutton').click(function() {{
            $.ajax({{
              type:'POST',
              url:'/face',
              data:"id=" + $(this).attr('id').substring(1) + "&csrf=" + "{csrf_token}",
              success: function() {{ location.reload(); }}
            }});
          }});
        }});
        </script>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
        <style>
        body {{
            padding-top: 120px;
            padding-bottom: 40px;
            background-color: #def;
            background-image: url('https://rare-gallery.com/thumbs/1138484-shadow-wall-texture-memes-light-darkness-screenshot.jpg');
            background-size: cover; /* Ensures the image covers the entire background */
            background-repeat: no-repeat; /* Prevents the image from repeating */
            background-position: center; /* Centers the image */
        }}
        .btn {{
           outline:0;
           border:none;
           border-top:none;
           border-bottom:none;
           border-left:none;
           border-right:none;
           box-shadow:inset 2px -3px rgba(0,0,0,0.15);
        }}
        .btn:focus {{
           outline:0;
           -webkit-outline:0;
           -moz-outline:0;
        }}
        .form-signin {{
            max-width: 560px;
            padding: 15px;
            margin: 0 auto;
            margin-top:50px;
        }}
        .form-signin .form-signin-heading, .form-signin {{
            margin-bottom: 10px;
        }}
        .form-signin .form-control {{
            position: relative;
            font-size: 16px;
            height: auto;
            padding: 10px;
            -webkit-box-sizing: border-box;
            -moz-box-sizing: border-box;
            box-sizing: border-box;
        }}
        .form-signin .form-control:focus {{
            z-index: 2;
        }}
        .form-signin input[type="text"] {{
            margin-bottom: -1px;
            border-bottom-left-radius: 0;
            border-bottom-right-radius: 0;
            border-top-style: solid;
            border-right-style: solid;
            border-bottom-style: none;
            border-left-style: solid;
            border-color: #000;
        }}
        .form-signin input[type="password"] {{
            margin-bottom: 10px;
            border-top-left-radius: 0;
            border-top-right-radius: 0;
            border-top-style: none;
            border-right-style: solid;
            border-bottom-style: solid;
            border-left-style: solid;
            border-color: rgb(0,0,0);
            border-top:1px solid rgba(0,0,0,0.08);
        }}
        .form-signin-heading {{
            color: #fff;
            text-align: center;
            text-shadow: 0 2px 2px rgba(0,0,0,0.5);
        }}
        .error {{
            color: #ccc;
            border-radius: 10px;
            background-color: #fcc;
            text-align: center;
            padding: 10px;
            padding-top: 20px;
            width: 300px;
            margin: 0 auto;
            border-style: solid;
        }}
        .error p {{
            color: #f00;
            font-size: 26px;
            padding: 0px;
        }}
        </style>
        </head>

        <body>

        <div id="fullscreen_bg" class="fullscreen_bg"></div>

         <div class="logo" style="width: 100%; background: url(http://shell.hackintro25.di.uoa.gr:30611/static/thefacebooklogo.png) no-repeat center center; height: 200px">
         </div>

        <div class="container">

            <form role="form" action="/login" method="post" class="form-signin">
            
            <h1 class="form-signin-heading text-muted">Sign In/Register</h1>
            <input id="email" name="user" type="text" class="form-control" placeholder="Username" required="" autofocus="">
            <input type="password" name="password" id="password" class="form-control" placeholder="Password" required="">
            <input type="hidden" name="csrf" value="{csrf_token}">
            <button class="btn btn-lg btn-primary btn-block" type="submit">
              Sign In
            </button>
            <button class="btn btn-lg btn-primary btn-block" type="submit" name="new" value="new">
              Register
            </button>
          </form>

        </div>

        </body></html>
        """)
        resp.set_cookie('auth', token)
        return resp

    # Serve the logged-in page if the cookie contains a user
    db = get_db()
    faces = db.execute("SELECT face_id, COUNT(username) as likes FROM likes GROUP BY face_id").fetchall()
    face_data = {face['face_id']: face['likes'] for face in faces}

    resp = make_response(f"""
    <html><head>
    <title>The Face Book</title>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script type="text/javascript">
    $(document).ready(function() {{
      $('.facebutton').click(function() {{
        $.ajax({{
          type:'POST',
          url:'/face',
          data:"id=" + $(this).attr('id').substring(1) + "&csrf=" + "{csrf_token}",
          success: function() {{ location.reload(); }}
        }});
      }});
    }});
    </script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <style>
    body {{
        padding-top: 120px;
        padding-bottom: 40px;
        background-color: #def;
        background-image: url('https://rare-gallery.com/thumbs/1138484-shadow-wall-texture-memes-light-darkness-screenshot.jpg');
        background-size: cover; /* Ensures the image covers the entire background */
        background-repeat: no-repeat; /* Prevents the image from repeating */
        background-position: center; /* Centers the image */
    }}
    .btn {{
       outline:0;
       border:none;
       border-top:none;
       border-bottom:none;
       border-left:none;
       border-right:none;
       box-shadow:inset 2px -3px rgba(0,0,0,0.15);
    }}
    .btn:focus {{
       outline:0;
       -webkit-outline:0;
       -moz-outline:0;
    }}
    .form-signin {{
        max-width: 560px;
        padding: 15px;
        margin: 0 auto;
        margin-top:50px;
    }}
    .form-signin .form-signin-heading, .form-signin {{
        margin-bottom: 10px;
    }}
    .form-signin .form-control {{
        position: relative;
        font-size: 16px;
        height: auto;
        padding: 10px;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
    }}
    .form-signin .form-control:focus {{
        z-index: 2;
    }}
    .form-signin input[type="text"] {{
        margin-bottom: -1px;
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
        border-top-style: solid;
        border-right-style: solid;
        border-bottom-style: none;
        border-left-style: solid;
        border-color: #000;
    }}
    .form-signin input[type="password"] {{
        margin-bottom: 10px;
        border-top-left-radius: 0;
        border-top-right-radius: 0;
        border-top-style: none;
        border-right-style: solid;
        border-bottom-style: solid;
        border-left-style: solid;
        border-color: rgb(0,0,0);
        border-top:1px solid rgba(0,0,0,0.08);
    }}
    .form-signin-heading {{
        color: #fff;
        text-align: center;
        text-shadow: 0 2px 2px rgba(0,0,0,0.5);
    }}
    .error {{
        color: #ccc;
        border-radius: 10px;
        background-color: #fcc;
        text-align: center;
        padding: 10px;
        padding-top: 20px;
        width: 300px;
        margin: 0 auto;
        border-style: solid;
    }}
    .error p {{
        color: #f00;
        font-size: 26px;
        padding: 0px;
    }}
    </style>
    </head>

    <body>
    <div id="fullscreen_bg" class="fullscreen_bg"></div>
    <div class="logo" style="width: 100%; background: url(http://shell.hackintro25.di.uoa.gr:30611/static/thefacebooklogo.png) no-repeat center center; height: 200px"></div>
    <div class="container" style="color:#bbb; padding:50px;">
      <a href="/logout" class="btn btn-lg btn-block btn-primary" role="button">Logout</a>
      <div class="page-header">
        <h1>Welcome, {user_info.get('user', '')}!</h1>
      </div>
      <div class="book">
        <h2>Faces</h2>
        <table>
          <tbody>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/19760.jpg"><figcaption>
            <button class="facebutton" id="f19760"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('19760', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/10235.jpg"><figcaption>
            <button class="facebutton" id="f10235"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('10235', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/16903.jpg"><figcaption>
            <button class="facebutton" id="f16903"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('16903', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/30316.jpg"><figcaption>
            <button class="facebutton" id="f30316"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('30316', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/27863.jpg"><figcaption>
            <button class="facebutton" id="f27863"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('27863', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/11406.jpg"><figcaption>
            <button class="facebutton" id="f11406"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('11406', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/19557.jpg"><figcaption>
            <button class="facebutton" id="f19557"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('19557', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/12488.jpg"><figcaption>
            <button class="facebutton" id="f12488"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('12488', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/10252.jpg"><figcaption>
            <button class="facebutton" id="f10252"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('10252', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/18646.jpg"><figcaption>
            <button class="facebutton" id="f18646"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('18646', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/12131.jpg"><figcaption>
            <button class="facebutton" id="f12131"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('12131', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/24811.jpg"><figcaption>
            <button class="facebutton" id="f24811"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('24811', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/18467.jpg"><figcaption>
            <button class="facebutton" id="f18467"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('18467', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/8799.jpg"><figcaption>
            <button class="facebutton" id="f8799"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('8799', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/16996.jpg"><figcaption>
            <button class="facebutton" id="f16996"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('16996', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/21713.jpg"><figcaption>
            <button class="facebutton" id="f21713"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('21713', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/32372.jpg"><figcaption>
            <button class="facebutton" id="f32372"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('32372', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/24865.jpg"><figcaption>
            <button class="facebutton" id="f24865"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('24865', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/12149.jpg"><figcaption>
            <button class="facebutton" id="f12149"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('12149', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/2269.jpg"><figcaption>
            <button class="facebutton" id="f2269"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('2269', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/6618.jpg"><figcaption>
            <button class="facebutton" id="f6618"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('6618', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/23814.jpg"><figcaption>
            <button class="facebutton" id="f23814"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('23814', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/9736.jpg"><figcaption>
            <button class="facebutton" id="f9736"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('9736', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/31053.jpg"><figcaption>
            <button class="facebutton" id="f31053"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('31053', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/25903.jpg"><figcaption>
            <button class="facebutton" id="f25903"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('25903', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/17502.jpg"><figcaption>
            <button class="facebutton" id="f17502"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('17502', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/15267.jpg"><figcaption>
            <button class="facebutton" id="f15267"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('15267', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/22028.jpg"><figcaption>
            <button class="facebutton" id="f22028"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('22028', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/25931.jpg"><figcaption>
            <button class="facebutton" id="f25931"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('25931', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/10568.jpg"><figcaption>
            <button class="facebutton" id="f10568"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('10568', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/26944.jpg"><figcaption>
            <button class="facebutton" id="f26944"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('26944', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/8588.jpg"><figcaption>
            <button class="facebutton" id="f8588"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('8588', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/29898.jpg"><figcaption>
            <button class="facebutton" id="f29898"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('29898', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/17422.jpg"><figcaption>
            <button class="facebutton" id="f17422"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('17422', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/25117.jpg"><figcaption>
            <button class="facebutton" id="f25117"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('25117', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/25798.jpg"><figcaption>
            <button class="facebutton" id="f25798"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('25798', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/14471.jpg"><figcaption>
            <button class="facebutton" id="f14471"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('14471', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/1001.jpg"><figcaption>
            <button class="facebutton" id="f1001"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('1001', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/28711.jpg"><figcaption>
            <button class="facebutton" id="f28711"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('28711', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/4096.jpg"><figcaption>
            <button class="facebutton" id="f4096"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('4096', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/24817.jpg"><figcaption>
            <button class="facebutton" id="f24817"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('24817', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/8470.jpg"><figcaption>
            <button class="facebutton" id="f8470"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('8470', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/6233.jpg"><figcaption>
            <button class="facebutton" id="f6233"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('6233', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/5201.jpg"><figcaption>
            <button class="facebutton" id="f5201"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('5201', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/3330.jpg"><figcaption>
            <button class="facebutton" id="f3330"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('3330', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/647.jpg"><figcaption>
            <button class="facebutton" id="f647"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('647', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/1637.jpg"><figcaption>
            <button class="facebutton" id="f1637"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('1637', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/5356.jpg"><figcaption>
            <button class="facebutton" id="f5356"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('5356', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/15735.jpg"><figcaption>
            <button class="facebutton" id="f15735"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('15735', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/2150.jpg"><figcaption>
            <button class="facebutton" id="f2150"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('2150', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/32162.jpg"><figcaption>
            <button class="facebutton" id="f32162"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('32162', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/27906.jpg"><figcaption>
            <button class="facebutton" id="f27906"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('27906', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/27828.jpg"><figcaption>
            <button class="facebutton" id="f27828"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('27828', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/3911.jpg"><figcaption>
            <button class="facebutton" id="f3911"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('3911', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/22687.jpg"><figcaption>
            <button class="facebutton" id="f22687"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('22687', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/12608.jpg"><figcaption>
            <button class="facebutton" id="f12608"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('12608', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/7228.jpg"><figcaption>
            <button class="facebutton" id="f7228"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('7228', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/20787.jpg"><figcaption>
            <button class="facebutton" id="f20787"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('20787', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/11064.jpg"><figcaption>
            <button class="facebutton" id="f11064"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('11064', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/9766.jpg"><figcaption>
            <button class="facebutton" id="f9766"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('9766', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/19373.jpg"><figcaption>
            <button class="facebutton" id="f19373"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('19373', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/8118.jpg"><figcaption>
            <button class="facebutton" id="f8118"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('8118', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/1002.jpg"><figcaption>
            <button class="facebutton" id="f1002"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('1002', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/3750.jpg"><figcaption>
            <button class="facebutton" id="f3750"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('3750', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/22978.jpg"><figcaption>
            <button class="facebutton" id="f22978"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('22978', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/15781.jpg"><figcaption>
            <button class="facebutton" id="f15781"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('15781', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/1840.jpg"><figcaption>
            <button class="facebutton" id="f1840"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('1840', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/26119.jpg"><figcaption>
            <button class="facebutton" id="f26119"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('26119', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/12922.jpg"><figcaption>
            <button class="facebutton" id="f12922"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('12922', 0)} faces!</figcaption></figure></td>
          </tr>
          <tr>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/1900.jpg"><figcaption>
            <button class="facebutton" id="f1900"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('1900', 0)} faces!</figcaption></figure></td>
            <td><figure><img src="http://shell.hackintro25.di.uoa.gr:30611/static/faces/288.jpg"><figcaption>
            <button class="facebutton" id="f288"><img src="http://shell.hackintro25.di.uoa.gr:30611/static/face.png"></button>
            {face_data.get('288', 0)} faces!</figcaption></figure></td>
          </tr>
          </tbody>
        </table>
      </div>
    </div>
    <footer>
    (Faces from <a href="https://www.bioid.com/About/BioID-Face-Database">https://www.bioid.com/About/BioID-Face-Database</a>)
    </footer>
    </body></html>
    """)
    return resp

@app.route('/login', methods=['POST'])
def login_or_register():
    user = request.form.get('user', '')
    pw = request.form.get('password', '')
    csrf_token = request.form.get('csrf', '')
    is_register = request.form.get('new') == 'new'

    # Validate CSRF token
    if not validate_csrf_token(csrf_token):
        return no_hacking_allowed()

    # Check if username or password fields are missing
    if not user or not pw:
        return no_hacking_allowed()

    # Check if username or password exceeds 2048 bytes
    if len(user) > 2048 or len(pw) > 2048:
        return no_hacking_allowed()

    db = get_db()

    if is_register:
        try:
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pw))
            db.commit()
        except sqlite3.IntegrityError:
            # Generate a new CSRF token for the "User exists" page
            new_csrf_token = generate_csrf_token()
            return f"""
            <html><head>
            <title>The Face Book</title>
            <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
            <script type="text/javascript">
            $(document).ready(function() {{
              $('.facebutton').click(function() {{
                $.ajax({{
                  type:'POST',
                  url:'/face',
                  data:"id="+$(this).attr('id').substring(1)+"&csrf={new_csrf_token}",
                  success: function() {{ location.reload(); }}
                }});
              }});
            }});
            </script>
            <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
            <style>
            body {{
                padding-top: 120px;
                padding-bottom: 40px;
                background-color: #def;
                background-image: url('https://rare-gallery.com/thumbs/1138484-shadow-wall-texture-memes-light-darkness-screenshot.jpg');
                background-size: cover; /* Ensures the image covers the entire background */
                background-repeat: no-repeat; /* Prevents the image from repeating */
                background-position: center; /* Centers the image */
            }}
            .btn {{
               outline:0;
               border:none;
               border-top:none;
               border-bottom:none;
               border-left:none;
               border-right:none;
               box-shadow:inset 2px -3px rgba(0,0,0,0.15);
            }}
            .btn:focus {{
               outline:0;
               -webkit-outline:0;
               -moz-outline:0;
            }}
            .form-signin {{
                max-width: 560px;
                padding: 15px;
                margin: 0 auto;
                margin-top:50px;
            }}
            .form-signin .form-signin-heading, .form-signin {{
                margin-bottom: 10px;
            }}
            .form-signin .form-control {{
                position: relative;
                font-size: 16px;
                height: auto;
                padding: 10px;
                -webkit-box-sizing: border-box;
                -moz-box-sizing: border-box;
                box-sizing: border-box;
            }}
            .form-signin .form-control:focus {{
                z-index: 2;
            }}
            .form-signin input[type="text"] {{
                margin-bottom: -1px;
                border-bottom-left-radius: 0;
                border-bottom-right-radius: 0;
                border-top-style: solid;
                border-right-style: solid;
                border-bottom-style: none;
                border-left-style: solid;
                border-color: #000;
            }}
            .form-signin input[type="password"] {{
                margin-bottom: 10px;
                border-top-left-radius: 0;
                border-top-right-radius: 0;
                border-top-style: none;
                border-right-style: solid;
                border-bottom-style: solid;
                border-left-style: solid;
                border-color: rgb(0,0,0);
                border-top:1px solid rgba(0,0,0,0.08);
            }}
            .form-signin-heading {{
                color: #fff;
                text-align: center;
                text-shadow: 0 2px 2px rgba(0,0,0,0.5);
            }}
            .error {{
                color: #ccc;
                border-radius: 10px;
                background-color: #fcc;
                text-align: center;
                padding: 10px;
                padding-top: 20px;
                width: 300px;
                margin: 0 auto;
                border-style: solid;
            }}
            .error p {{
                color: #f00;
                font-size: 26px;
                padding: 0px;
            }}
            </style>
            </head>

            <body>

            <div id="fullscreen_bg" class="fullscreen_bg"></div>

            <div class="logo" style="width: 100%; background: url(http://shell.hackintro25.di.uoa.gr:30611/static/thefacebooklogo.png) no-repeat center center; height: 200px">
            </div>

            <div class="container">

                <form role="form" action="/login" method="post" class="form-signin">
                
                  <div class="error"><p>User exists</p></div>
                
                <h1 class="form-signin-heading text-muted">Sign In/Register</h1>
                <input id="email" name="user" type="text" class="form-control" placeholder="Username" required="" autofocus="">
                <input type="password" name="password" id="password" class="form-control" placeholder="Password" required="">
                <input type="hidden" name="csrf" value="{new_csrf_token}">
                <button class="btn btn-lg btn-primary btn-block" type="submit">
                  Sign In
                </button>
                <button class="btn btn-lg btn-primary btn-block" type="submit" name="new" value="new">
                  Register
                </button>
              </form>

            </div>

            </body></html>
            """

    row = db.execute("SELECT password FROM users WHERE username = ?", (user,)).fetchone()
    if row and row['password'] == pw:
        token = request.cookies.get('auth')
        user_info = verify_token(token) if token else {'tick': 1}

        # Update the token with login details
        user_info.update({'admin': 0, 'user': user, 'tick': user_info.get('tick', 0) + 1})
        token = create_token(user_info)
        resp = make_response(redirect('/'))
        resp.set_cookie('auth', token)
        return resp

    # Generate a new CSRF token for the bad login page
    new_csrf_token = generate_csrf_token()
    return f"""
    <html><head>
    <title>The Face Book</title>
    <script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
    <script type="text/javascript">
    $(document).ready(function() {{
      $('.facebutton').click(function() {{
        $.ajax({{
          type:'POST',
          url:'/face',
          data:"id="+$(this).attr('id').substring(1)+"&csrf={new_csrf_token}",
          success: function() {{ location.reload(); }}
        }});
      }});
    }});
    </script>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.2.0/css/bootstrap.min.css">
    <style>
    body {{
        padding-top: 120px;
        padding-bottom: 40px;
        background-color: #def;
        background-image: url('https://rare-gallery.com/thumbs/1138484-shadow-wall-texture-memes-light-darkness-screenshot.jpg');
        background-size: cover; /* Ensures the image covers the entire background */
        background-repeat: no-repeat; /* Prevents the image from repeating */
        background-position: center; /* Centers the image */
    }}
    .btn {{
       outline:0;
       border:none;
       border-top:none;
       border-bottom:none;
       border-left:none;
       border-right:none;
       box-shadow:inset 2px -3px rgba(0,0,0,0.15);
    }}
    .btn:focus {{
       outline:0;
       -webkit-outline:0;
       -moz-outline:0;
    }}
    .form-signin {{
        max-width: 560px;
        padding: 15px;
        margin: 0 auto;
        margin-top:50px;
    }}
    .form-signin .form-signin-heading, .form-signin {{
        margin-bottom: 10px;
    }}
    .form-signin .form-control {{
        position: relative;
        font-size: 16px;
        height: auto;
        padding: 10px;
        -webkit-box-sizing: border-box;
        -moz-box-sizing: border-box;
        box-sizing: border-box;
    }}
    .form-signin .form-control:focus {{
        z-index: 2;
    }}
    .form-signin input[type="text"] {{
        margin-bottom: -1px;
        border-bottom-left-radius: 0;
        border-bottom-right-radius: 0;
        border-top-style: solid;
        border-right-style: solid;
        border-bottom-style: none;
        border-left-style: solid;
        border-color: #000;
    }}
    .form-signin input[type="password"] {{
        margin-bottom: 10px;
        border-top-left-radius: 0;
        border-top-right-radius: 0;
        border-top-style: none;
        border-right-style: solid;
        border-bottom-style: solid;
        border-left-style: solid;
        border-color: rgb(0,0,0);
        border-top:1px solid rgba(0,0,0,0.08);
    }}
    .form-signin-heading {{
        color: #fff;
        text-align: center;
        text-shadow: 0 2px 2px rgba(0,0,0,0.5);
    }}
    .error {{
        color: #ccc;
        border-radius: 10px;
        background-color: #fcc;
        text-align: center;
        padding: 10px;
        padding-top: 20px;
        width: 300px;
        margin: 0 auto;
        border-style: solid;
    }}
    .error p {{
        color: #f00;
        font-size: 26px;
        padding: 0px;
    }}
    </style>
    </head>

    <body>

    <div id="fullscreen_bg" class="fullscreen_bg"></div>

    <div class="logo" style="width: 100%; background: url(http://shell.hackintro25.di.uoa.gr:30611/static/thefacebooklogo.png) no-repeat center center; height: 200px">
    </div>

    <div class="container">

        <form role="form" action="/login" method="post" class="form-signin">
        
          <div class="error"><p>Bad Login</p></div>
        
        <h1 class="form-signin-heading text-muted">Sign In/Register</h1>
        <input id="email" name="user" type="text" class="form-control" placeholder="Username" required="" autofocus="">
        <input type="password" name="password" id="password" class="form-control" placeholder="Password" required="">
        <input type="hidden" name="csrf" value="{new_csrf_token}">
        <button class="btn btn-lg btn-primary btn-block" type="submit">
          Sign In
        </button>
        <button class="btn btn-lg btn-primary btn-block" type="submit" name="new" value="new">
          Register
        </button>
      </form>

    </div>

    </body></html>
    """

@app.route('/logout', methods=['GET'])
def logout():
    token = request.cookies.get('auth')
    user_info = verify_token(token) if token else {'tick': 1}

    # Increment the tick value
    new_payload = {'tick': user_info.get('tick', 1) + 1}

    # Create a new token with the updated tick value
    token = create_token(new_payload)
    resp = make_response(redirect('/'))
    resp.set_cookie('auth', token)
    return resp

@app.route('/face', methods=['POST'])
def like_face():
    face_id = request.form.get('id', '')
    csrf_token = request.form.get('csrf', '')
    token = request.cookies.get('auth')
    user_info = verify_token(token)

    if not user_info or 'user' not in user_info:
        return json.dumps({"success": False})
    
    # Validate CSRF token
    if not validate_csrf_token(csrf_token):
        return no_hacking_allowed(user_info)

    # Check if face_id is more than 16 bytes long
    if len(face_id) > 16:
        return no_hacking_allowed(user_info)

    username = user_info['user']
    db = get_db()

    # Check if the user has already liked the face
    row = db.execute("SELECT 1 FROM likes WHERE username = ? AND face_id = ?", (username, face_id)).fetchone()
    if row:
        return json.dumps({"success": False})  # User already liked the face

    # Insert the like into the database
    db.execute("INSERT INTO likes (username, face_id) VALUES (?, ?)", (username, face_id))
    db.commit()
    return json.dumps({"success": True})

# This doesnt exist in the original facebook 2 just added it as a way to 
# kill the server when I accidently disconnect from my ssh session without closing it
@app.route('/kill', methods=['GET'])
def kill_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        return "<h>Server shutdown not supported</h>", 500
    func()
    return "<h>Server shutting down...</h>"

# --- DB init (only if it doesn't exist) ---

def init_db():
    if not os.path.exists(DB_FILE):
        db = get_db()
        db.execute("CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)")
        db.execute("CREATE TABLE likes (username TEXT, face_id TEXT, PRIMARY KEY (username, face_id))")
        db.commit()
        db.close()

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=1338, debug=True)
