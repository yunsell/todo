import sys, os, mariadb
from flask import Flask, render_template, request, redirect , url_for
app = Flask(__name__)


def get_conn():
    conn = mariadb.connect(
        user="root",
        password="1234",
        host="localhost",
        port=3300,
        database="todo"
    )
    return conn

@app.route("/")
def todo():

    sql = """select num,content from todolist;"""

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        test = cur.fetchall()

    finally:
        if conn:
            conn.close()

    return render_template("/todo.html", content=test)


@app.route("/content", methods=['POST',])
def content():
    if request.method == 'POST':
        element = request.form['name']
        print(element)
        conn = get_conn()
        sql = "INSERT INTO todo.todolist (content) VALUES ('{}')".format(element)

        cur = conn.cursor()
        cur.execute(sql)

        conn.commit()

        if conn:
            conn.close()

        return redirect(url_for('todo'))

@app.route("/delete", methods=['POST','GET'])
def delelte():
    # if request.method == 'POST':

    num = request.args.get('id', type=int)
    conn = get_conn()
    sql = "DELETE FROM todolist WHERE num={};".format(num)

    cur = conn.cursor()
    cur.execute(sql)

    conn.commit()

    if conn:
        conn.close()

    return redirect(url_for('todo'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')