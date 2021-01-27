from flask import Flask, render_template, request, redirect
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, EqualTo, length
import email_validator

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Cant_say'

class inputForm(Form):
    fname = StringField('fname', validators=[InputRequired()])
    lname = StringField('lname', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email()])
    pass1 = PasswordField('pass1', validators=[InputRequired(), length(min=6, max=20)])
    cpass = PasswordField('cpass', validators=[InputRequired(), length(min=6, max=20), EqualTo('pass1', message='Passwords must match')])


@app.route('/', methods=['POST', 'GET'])
def home():
    form = inputForm()
    if request.method=="POST":
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        pass1 = form.pass1.data
        cpass = form.cpass.data
        print(fname, lname, email, pass1, cpass)
        return redirect('/')
    return render_template("home.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
