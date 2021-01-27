from flask import Flask, render_template
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import *

app = Flask(__name__)
@app.route('/')
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
