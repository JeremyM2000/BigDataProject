from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.secret_key = 'your_secret_key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password
        
users = {
    'user1': User('1', 'user1', 'password1'),
    'user2': User('2', 'user2', 'password2')
}

@login_manager.user_loader
def load_user(user_id):
    for user in users.values():
        if user.id == user_id:
            return user
    return None

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Remember me')

@app.route("/")
def home():
    return render_template('home.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = users.get(form.username.data)
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            flash('Logged in successfully.')
            next = request.args.get('next')
            if not next or not next.startswith('/'):
                next = url_for('home')
            return redirect(next)
        else:
            flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('home'))

@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.username

if __name__ == "__main__":
    app.run(debug=True)
