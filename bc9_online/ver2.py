from flask import Flask, request, render_template
from flask_wtf import FlaskForm
from flask_wtf.csrf import CSRFProtect
from flask_wtf.recaptcha import RecaptchaField
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired

DEBUG = True
WTF_CSRF_SECRET_KEY = ""
RECAPTCHA_PUBLIC_KEY = "6LcbytEeAAAAAOgX2XjYPWCE1q4rRXD601lkBp-k"
RECAPTCHA_PRIVATE_KEY = ""
# RECAPTCHA_API_SERVER = ""
RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = WTF_CSRF_SECRET_KEY
csrf = CSRFProtect(app)

class MyForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    #recaptcha = RecaptchaField()
    # Uncomment above when ready

@csrf.exempt
@app.route("/")
def index(form=None):
    if form is None:
        form = MyForm()
        return render_template('form.html', form=form)
    return render_template("success.html", form=form)

@app.route('/submit', methods=['POST'])
def submit():
    form = MyForm()
    if form.validate_on_submit():
        return render_template('success.html', form=form)
    return render_template('form.html', form=form)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
