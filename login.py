from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.fields.html5 import EmailField
from flask_pymongo import pymongo

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Cant_say'

class inputForm(Form):
    fname = StringField('fname', validators=[DataRequired()])
    lname = StringField('lname', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    pass1 = PasswordField('pass1', validators=[DataRequired()])
    sub = SubmitField('Sign Up')

class inputFormlogin(Form):
    email = EmailField('email', validators=[DataRequired(), Email()])
    pass1 = PasswordField('pass1', validators=[DataRequired()])
    sub = SubmitField('Login')

CONNECTION_STRING = "mongodb+srv://VIT_Admin:<password>@vitdiaries.tpuku.mongodb.net/CouponShare?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('CouponShare')
user_collection = pymongo.collection.Collection(db, 'Users')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    form = inputForm()
    if request.method=="POST":
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        pass1 = form.pass1.data
        # print(fname, lname, email, pass1)
        if form.validate_on_submit():
            return("Submitted")
        else:
            new=''
            for s in pass1:
                n = ((ord(s) + 237)**2)%26
                new+=chr(n)
            user_collection.insert_one({'First Name': fname, 'Last Name': lname, 'Email': email, 'Password': new})
        return "Logged in"
    return render_template("signup.html", form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    form_login = inputFormlogin()
    if request.method=="POST":
        email = form_login.email.data
        pass1 = form_login.pass1.data
        if form_login.validate_on_submit():
            return("Submitted")
        else:
            new=''
            for s in pass1:
                n = ((ord(s) + 237)**2)%26
                new+=chr(n)
            filter_dict = {"Email": email, "Password": new}
            # print(filter_dict)
            if user_collection.count_documents(filter_dict):
                print("item is existed")
                flash("item is existed")
                return "Logged in"
            else:
                print("item is not existed")
                flash('Invalid Credentials')
                return redirect('/login')
    return render_template("login.html", form_login=form_login)



if __name__ == "__main__":
    app.run(debug=True)
