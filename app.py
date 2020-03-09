from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, RadioField, validators

app = Flask(__name__)

app.config['SECRET_KEY'] = 'demo_secret_key'

class RegistrationForm(FlaskForm):
    name = StringField("NAME", [
        validators.DataRequired()
    ])
    email = StringField("EMAIL", [
        validators.Email()
    ])
    password = PasswordField("PASSWORD", [
        validators.DataRequired(),
        validators.Length(min=10),
        validators.EqualTo("confirm_password", message="PASSWORDS MUST MATCH!")])
    confirm_password = PasswordField("CONFIRM PASSWORD")
    if password == confirm_password:
        flash("PASSWORDS MATCHED.")
    m_or_f = RadioField("ARE YOU MALE OR FEMALE?", [
        validators.DataRequired(),
    ],
    choices=[("mood_one", "MALE"), ("mood_two", "FEMALE")],)
    t_and_c = BooleanField("I AGREE TO THE TERMS AND CONDITIONS.", [
        validators.DataRequired(),
    ])
    submit = SubmitField("SIGN UP")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/registration', methods = ["GET", "POST"])
def register():
    registrationform = RegistrationForm(request.form)
    if request.method == 'POST' and registrationform.validate():
        session["name"] = registrationform.name.data
        session["m_or_f"] = registrationform.m_or_f.data
        return redirect(url_for('registrationsuccessful'))
    return render_template('register.html', form = registrationform)

@app.route('/user/registration/registrationsuccessful')
def registrationsuccessful():
    return render_template('registration_successful.html')

@app.route('/user/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run()
