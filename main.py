import mariadb, sys, os
from flask import Flask, render_template, request, redirect , url_for, session

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
    if 'NUMBER' in session:
        r_num = session['NUMBER']
        alert = """
                <script>
                    alert("잘못된 접근입니다.")
                </script>
                """
        return render_template("/", alert=alert)
    return render_template("/login.html")

@app.route("/lo_gin", methods=['POST'])
def check_id():
    insert_id = request.form['id']
    insert_pw = request.form['pw']
    login_flag = False

    result = ""

    sql = "SELECT ID, PW, NUMBER FROM MEMBER WHERE ID = '{}'".format(insert_id)
    try:
        conn = get_conn()
        cur = conn.cursor()
        cur.execute(sql)

        for (ID, PW, NUMBER) in cur:
            result = "{0},{1}".format(ID, PW)

            if ID == insert_id and PW == insert_pw :
                session.clear()
                session['id'] = request.form['id']
                session['NUMBER'] = NUMBER
                login_flag = True
                break
    except mariadb.Error as e:
        print("ERR: {}".format(e))
        sys.exit(1)
    except TypeError as e:
        result = ""
    if conn:
        conn.close()
        result = """
        <script>
        alert("아이디 또는 패스워드를 확인 하세요.");
        </script>
        """
    if login_flag:
        return render_template('/login.html')
    else:
        return render_template('/login.html', content=result)


@app.route("/signup")
def sign_up():
    return render_template("/signup.html")

@app.route("/sign_up", methods=['POST'])
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
    app.secret_key = 'app secret key'
    app.run(host='0.0.0.0')