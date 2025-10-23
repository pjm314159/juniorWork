import jmcomic
from flask import Flask, request, redirect, url_for, render_template, session, send_from_directory
from os import listdir
from os import urandom
from os.path import join, getmtime
from sqlite3 import connect
from sys import path
from provide_data import *
from provide_data import jm
path.append("provide_data")
app = Flask(__name__)
app.config.from_pyfile("static/settings.py")
app.config['SECRET_KEY'] = urandom(24)
coon = connect("static/content.db", check_same_thread=False)
cur = coon.cursor()
pl = ["syjszpc", 'xxmh88', "realPeople", "goddess", "scores","jm"]
ql = ["demo1", "demo2", "demo3", "demo4", "demo5","jm"]
co = {i: {x[1]: x[0] for x in cur.execute(f"SELECT * from {i}")} for i in pl}


# log = getLogger("werkzeug")
# log.setLevel(ERROR)

@app.route("/", methods=["POST", "GET"])
def login():
    if session.get('user') == "ardmin" and session.get('password') == "314159":
        return redirect(url_for('choice'))
    return render_template("login.html")


@app.route("/worse/<string:name>")
def worse(name):
    return f"Worse\n{name}"


@app.route("/index", methods=["GET"])
def index():
    user = session.get('user')
    password = session.get('password')

    if user == "admin" and password == "314159":
        text = listdir('static/image')
        if text:
            urls = [''] * len(text)
            for i in range(len(text)):
                urls[i] = f"image/{text[i]}"
            p = render_template('index.html', urls=urls, text=text, p=range(len(urls)))
        else:
            p = redirect(url_for("worse",name="not find"))
    else:
        p = redirect(url_for("worse",name="password or username worse"))
    return p


@app.route("/image/<string:name>", methods=["POST", "GET"])
def index_image(name):
    user = session.get('user')
    password = session.get('password')
    if user == "admin" and password == "314159":
        text = sorted(listdir(f'static/image/{name}'), key=lambda x: getmtime(join(f'static/image/{name}', x)))
        if text:
            urls = [''] * len(text)
            for i in range(len(text)):
                urls[i] = f"{name}/{text[i]}"
            p = render_template('index.html', urls=urls, text=text, p=range(len(urls)))
        else:
            p = redirect(url_for("worse", name="not find"))
    else:
        p = redirect(url_for("worse", name="password or username worse"))
    return p


@app.route("/image/<string:name>/<string:img>/<string:a>", methods=["GET"])
def get_img(name, img, a):
    user = session.get('user')
    password = session.get('password')
    if user == "admin" and password == "314159":
        p = f"static/image/{name}/{img}/{a}"
    else:
        p = redirect(url_for("worse", name="password or username worse"))
    return redirect(url_for(p))


@app.route("/image/<string:name>/<string:img>", methods=["POST", "GET"])
def index_img(name, img):
    user = session.get('user')
    password = session.get('password')

    if user == "admin" and password == "314159":
        text = listdir(f'static/image/{name}/{img}')
        if text:
            urls = [''] * len(text)
            for i in range(len(text)):
                urls[i] = f'image/{name}/{img}/{text[i]}'
            if name != "local":
                b = co[name].get(img)
                if not b:
                    b = co["scores"].get(img)
                    if not b:
                        b = ""
            else:
                b = ""
            p = render_template('img.html', urls=urls, a=img, p=b)
        else:
            p = redirect(url_for("worse", name="not find"))
    else:
        p = redirect(url_for("worse", name="password or username worse"))
    return p


@app.route("/choice", methods=["POST", "GET"])
def choice():
    if request.method == "POST":
        user = request.form['user']
        password = request.form["password"]
        session['user'] = user
        session['password'] = password
    else:
        user = session.get('user')
        password = session.get('password')
    if user == "admin" and password == "314159":
        urls = ['index', 'provide_data']
        text = ['read', 'write']
        p = render_template('index.html', urls=urls, text=text, p=range(len(urls)))
    else:
        p = redirect(url_for("worse", name="password or username worse"))
    return p


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.route('/provide_data', methods=["POST", "GET"])
def provide_data():
    user = session.get('user')
    password = session.get('password')
    if user == "admin" and password == "314159":
        p = render_template("read_data.html", p=range(len(ql)), lp=ql)
    else:
        p = redirect(url_for("worse", name="password or username worse"))
    return p


@app.route('/image/data', methods=["POST"])
def data_handle():
    user = session.get('user')
    password = session.get('password')
    url = request.form['url']
    method = request.form["method"]
    p = "worse"
    if user == "admin" and password == "314159":
        try:
            if method == '1':
                a = demo1.A(url)
                a.dl()
            elif method == '2':
                a = demo2.A(url)
                a.main()
                co["syjszpc"][a.sp.catalog] = url
            elif method == '3':
                a = demo3.A(url)
                a.main()
                co["xxmh88"][a.sp.catalog] = url
            elif method == '4':
                a = demo4.A(url)
                a.main()
                co["realPeople"][a.sp.catalog] = url
            elif method == "5":
                a = demo5.A(url)
                a.main()
                co["realPeople"][a.sp.catalog] = url
            elif method == '6':
                a = jm.A(url)
                a.jmOption = "static\jmOption.yml"
                a.create()
                a.download()
            else:
                return "It isn't in"
            try:
                p = 'success: ' + ql[int(method)-1]
            except:
                p = 'failure'
        except Exception as e:
            p = str(e)
    return p


if __name__ == "__main__":
    app.run(host='10.44.246.162', port=5000)