from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.fields.html5 import EmailField
from flask_pymongo import pymongo
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

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

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

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
            if user_collection.count_documents({"Email": email}):
                return "User already Exists!"
            else:
                cipher = generate_password_hash(pass1, method='sha256')
                user_collection.insert_one({'First Name': fname, 'Last Name': lname, 'Email': email, 'Password': cipher})
                return render_template('index.html', fname = fname, lname = lname)
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
            user = user_collection.find_one({"Email":email})
            if check_password_hash(user['Password'], pass1):
                print("item is existed")
                return render_template('index.html', fname = user['First Name'], lname = user['Last Name'])
            else:
                print("item is not existed")
                flash('Invalid Credentials')
                return redirect('/login')
    return render_template("login.html", form_login=form_login)

@app.route('/home')
@login_required
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
