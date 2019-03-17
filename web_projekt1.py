from flask import Flask, redirect, render_template, session, flash, url_for, request
import os
from forms import LoginForm
from users_model import UsersModel
from db import DB
from news_model import NewsModel

app = Flask(__name__)
app.config.from_object('config')
db = DB()
UsersModel(db.get_connection()).init_table()
NewsModel(db.get_connection()).init_table()


@app.route('/')
@app.route('/index')
def index():
    user = 'nobody'
    id = 'nobody'
    news_model = NewsModel(db.get_connection())
    cont = news_model.get_all()
    if 'username' in session:
        name = 'static/img/' + str(session['user_id']) + '.jpeg'
        if os.path.isfile(name):
            session['picture'] = name
        id = str(session['user_id'])
        user = session['username']
    return render_template("index.html", username=user, avatar=session['picture'], news=cont)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.id.data
        passw = form.passw.data
        pict = 'static/img/nobody.jpeg'
        user_model = UsersModel(db.get_connection())
        user_model.insert(user, passw, pict)
        exists = user_model.exists(user, passw)
        session['username'] = user
        session['user_id'] = exists[1]
        session['picture'] = 'static/img/nobody.jpeg'
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    session.pop('username', 0)
    session.pop('user_id', 0)
    session['picture'] = 'static/img/nobody.jpeg'
    return redirect('/index')


@app.route('/user')
def user():
    if 'username' not in session:
        return redirect('/index')
    user = session['username']
    id = session['user_id']
    avatar = session['picture']
    return render_template('user.html', username=user, avatar=avatar)


@app.route('/avatar/<action>', methods=['POST', 'GET'])
def avatar(action):
    if action == 'add':
        if request.method == 'GET':
            return render_template('avatar.html')
        elif request.method == 'POST':
            f = request.files['file']
            f = f.read()
            session['picture'] = 'static/img/' + str(session['user_id']) + '.jpeg'
            if os.path.isfile(session['picture']):
                os.remove(session['picture'])
            d = open(session['picture'], 'wb')
            d.write(f)
            d.close()
    else:
        nm = UsersModel(db.get_connection())
        a = nm.get(session['user_id'])
        nam = a[0]
        nm.update('static/img/nobody.jpeg', nam)
        if session['picture'] != 'static/img/nobody.jpeg':
            os.remove(session['picture'])
        session['picture'] = 'static/img/nobody.jpeg'
    return redirect('/user')


@app.route('/add_some', methods=['GET', 'POST'])
def add_some():
    if request.method == 'GET':
        return render_template('news.html')
    elif request.method == 'POST':
        nazv = request.form['nazv']
        about = request.form['about']
        col = request.form['t']
        f = request.files['file']
        f = f.read()
        name = 'static/img/' + nazv + '.jpeg'
        d = open(name, 'wb')
        d.write(f)
        d.close()
        news_model = NewsModel(db.get_connection())
        news_model.insert(nazv, about, col)
        return redirect('/index')


@app.route('/del_new/<int:news_id>', methods=['GET', 'POST'])
def del_new(news_id):
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect('/index')


@app.route('/buy/<int:news_id>', methods=['GET', 'POST'])
def buy(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    a = nm.get(news_id)
    if a[0] == 0:
        nm.delete(news_id)
        return 'Нет в наличие'
    else:
        if request.method == 'GET':
            return render_template('buy.html', col=a[0])
        elif request.method == 'POST':
            count = request.form['t']
            d = a[0] - int(count)
            nm.update(d, news_id)
            return redirect('/index')


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
