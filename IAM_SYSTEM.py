from flask import Flask, render_template, redirect, url_for, flash, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pyotp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///iam_system.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User Roles
ROLE_USER = 'User'
ROLE_ADMIN = 'Admin'
ROLE_GUEST = 'Guest'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(50), nullable=False, default=ROLE_GUEST)
    otp_secret = db.Column(db.String(16), nullable=False, default=pyotp.random_base32())

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        role = request.form['role'] if 'role' in request.form else ROLE_GUEST
        user = User(username=username, password=password, role=role)
        db.session.add(user)
        db.session.commit()
        flash('User registered successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            session['otp_verified'] = False
            session['user_id'] = user.id
            return redirect(url_for('mfa'))
        flash('Login failed. Check username and password.', 'danger')
    return render_template('login.html')

@app.route('/mfa', methods=['GET', 'POST'])
def mfa():
    user = User.query.get(session['user_id'])
    totp = pyotp.TOTP(user.otp_secret)
    if request.method == 'POST':
        token = request.form['token']
        if totp.verify(token):
            session['otp_verified'] = True
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        flash('Invalid MFA token.', 'danger')
    return render_template('mfa.html', otp_secret=user.otp_secret)

@app.route('/dashboard')
@login_required
def dashboard():
    if not session.get('otp_verified'):
        return redirect(url_for('mfa'))
    return render_template('dashboard.html', role=current_user.role)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
