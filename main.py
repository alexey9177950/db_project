import sqlite3
import os
from os.path import join
from random import randint
from flask import Flask, escape, request, render_template, make_response

SRC_PATH = os.path.dirname(os.path.realpath(__file__))
app = Flask(__name__, static_url_path='/static')
N_ERR_PICS = 5

def arg_missing(argname):
    return (argname not in request.args) or (request.args[argname] == "")


def run_sql(query, params=[], commit=False):
    connection = sqlite3.connect(os.path.join(SRC_PATH, "board.db"))
    cursor = connection.cursor()
    if type(query) == str:
        cursor.execute(query, params)
    else:
        for cmd in query:
            cursor.execute(cmd)
    res = cursor.fetchall()
    if commit:
        connection.commit()
    connection.close()
    return res


def init_db():
    db_path = join(SRC_PATH, 'board.db')
    if os.path.isfile(db_path):
        return
    commands = open(join(SRC_PATH, "init-db.sql")).read().split('\n\n')
    run_sql(commands, commit=True)


def error_page(message):
    return render_template('error.html', msg=message, ind=randint(1, N_ERR_PICS))


@app.route('/')
def main_page():
    data = run_sql("SELECT thread_id, op_text, header from threads")[::-1]
    return render_template('main.html', data=data)


@app.route('/create_thread')
def create_thread():
    if arg_missing('msg_text') or arg_missing('header'):
        return error_page("Пустой заголовок или пустое сообщение.")
    header, txt = request.args['header'], request.args['msg_text']
    run_sql("INSERT INTO threads (header, op_text) VALUES (?, ?);", (header, txt), commit=True)
    return render_template("create_ok.html", link="..")


@app.route('/thread')
def view_thread():
     try:
        t_id = int(request.args['t_id'])
     except:
        return error_page("Неправильный номер треда")
     
     try:
        t_id, op_msg, header = run_sql('SELECT thread_id, op_text, header FROM threads WHERE thread_id=?', [t_id])[0]
     except:
        return error_page("Неправильный номер треда")
     posts = run_sql('SELECT text FROM posts WHERE thread_id=?', [str(t_id)])
     posts = [i[0] for i in posts]
     return render_template('thread.html', t_id=t_id, op_msg=op_msg, header=header, posts=posts)


@app.route('/post')
def post_msg():
    if arg_missing('msg_text') or arg_missing('t_id'):
        return error_page("Пустое сообщение или не указан номер треда")
    t_id = request.args['t_id']
    txt = request.args['msg_text']
    try:
        run_sql("INSERT INTO posts (thread_id, text) VALUES (?, ?);", (t_id, txt), commit=True)
    except:
        return error_page("Неправильный номер треда")
    link = "../thread?t_id=" + t_id
    return render_template("msg_ok.html", link=link)


init_db()
app.run()
