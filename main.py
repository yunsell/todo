import mariadb
from flask import Flask, render_template, request, redirect , url_for
app = Flask(__name__)


def get_conn():
    conn = mariadb.connect(
        user="root",
        password="1234",
        host="localhost",
        port=3300,
        database="test"
    )
    return conn

@app.route("/") # 메인화면
def todo():

    sql = """select NUMBER,CONTENT from todolist;"""

    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)
        test = cur.fetchall()

    finally:
        if conn:
            conn.close()

    return render_template("/todo.html", content=test)

@app.route("/login")
def login():
    return render_template("/login.html")

@app.route('/signup')
def sign_up():
    return render_template("/signup.html")

@app.route('/sign_up', methods=['POST'])
def signup():

    if request.method == 'POST':
        new_id = request.form["ID"]
        new_pw = request.form["PW"]
        new_name = request.form["NAME"]
        new_phone = request.form["PHONE"]

        conn = get_conn()
        sql = "INSERT INTO member (ID, PW, NAME, PHONE) VALUES ('{0}', '{1}', '{2}', '{3}')".format(new_id, new_pw, new_name, new_phone)
        
        cur = conn.cursor()
        cur.execute(sql)
        
        conn.commit()
        
        if conn:
            conn.close()

        return redirect(url_for('login'))

@app.route("/content", methods=['POST']) # 내용표시
def content():
    if request.method == 'POST':
        element = request.form['content']
        print(element)
        conn = get_conn()
        sql = "INSERT INTO todolist (CONTENT) VALUES ('{}')".format(element)
        ####### 아이디 값 적용시켜야 글 올라감 #########
        cur = conn.cursor()
        cur.execute(sql)

        conn.commit()

        if conn:
            conn.close()

        return redirect(url_for('todo'))

@app.route("/delete", methods=['POST','GET']) # 글삭제
def delelte():
    # if request.method == 'POST':

    num = request.args.get('id', type=int)
    conn = get_conn()
    sql = "DELETE FROM todolist WHERE num={};".format(num)
    ####### 아이디 값 적용시켜야 글 삭제됨 #########
    cur = conn.cursor()
    cur.execute(sql)

    conn.commit()

    if conn:
        conn.close()

    return redirect(url_for('todo'))


if __name__ == "__main__":
    app.run(host='0.0.0.0')