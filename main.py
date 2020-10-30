import sys, os
from flask import Flask, render_template, request, session
app = Flask(__name__)

@app.route("/")
def todo():
    return render_template("/todo.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0')