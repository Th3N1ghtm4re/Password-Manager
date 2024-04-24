from flask import Flask, request, redirect, url_for, session, render_template
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///credentials.db'
db = SQLAlchemy(app)

class Credential(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    website = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)

valid_username_hash = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
valid_password_hash = "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"

@app.route('/')
def index():
    session.clear()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        password_hash = hashlib.sha256(password.encode()).hexdigest()
        username_hash = hashlib.sha256(username.encode()).hexdigest()

        if username_hash == valid_username_hash and password_hash == valid_password_hash:
            session['username'] = username
            return redirect(url_for('main'))
        else:
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/main', methods=['GET', 'POST'])
def main():
    if 'username' in session:
        if request.method == 'POST':
            website = request.form['website']
            username = request.form['username']
            password = request.form['password']
            new_credential = Credential(website=website, username=username, password=password)
            db.session.add(new_credential)
            db.session.commit()
            return redirect(url_for('main'))

        stored_credentials = Credential.query.all()
        return render_template('main.html', logout_url=url_for('logout'), stored_credentials=stored_credentials)
    else:
        return redirect(url_for('login'))
    
@app.route('/add_credentials', methods=['POST'])
def add_credentials():
    if 'username' in session:
        if request.method == 'POST':
            website = request.form['website']
            username = request.form['username']
            password = request.form['password']
            new_credential = Credential(website=website, username=username, password=password)
            db.session.add(new_credential)
            db.session.commit()
    return redirect(url_for('main'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete_credential(id):
    if 'username' in session:
        credential = Credential.query.get(id)
        if credential:
            db.session.delete(credential)
            db.session.commit()
    return redirect(url_for('main'))

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5001)