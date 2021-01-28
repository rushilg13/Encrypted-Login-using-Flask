from flask import Flask, render_template, request, redirect
from flask_wtf import Form
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from wtforms.fields.html5 import EmailField
from flask_pymongo import pymongo
import cryptocode

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Cant_say'

class inputForm(Form):
    fname = StringField('fname', validators=[DataRequired()])
    lname = StringField('lname', validators=[DataRequired()])
    email = EmailField('email', validators=[DataRequired(), Email()])
    pass1 = PasswordField('pass1', validators=[DataRequired()])
    sub = SubmitField('Sign Up')

CONNECTION_STRING = "mongodb+srv://VIT_Admin:pizza@vitdiaries.tpuku.mongodb.net/CouponShare?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('CouponShare')
user_collection = pymongo.collection.Collection(db, 'Users')

@app.route('/', methods=['POST', 'GET'])
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
            ciphertext = cryptocode.encrypt(pass1,"mysecretkey")
            # decrypttext = cryptocode.decrypt(ciphertext, "mysecretkey")
            user_collection.insert_one({'First Name': fname, 'Last Name': lname, 'Email': email, 'Password': ciphertext})
        return "Logged in"
    return render_template("signup.html", form=form)

if __name__ == "__main__":
    app.run(debug=True)
