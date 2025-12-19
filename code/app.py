import os
from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_socketio import SocketIO

# Настройка путей относительно папки code
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

app = Flask(__name__, 
            template_folder=os.path.join(BASE_DIR, 'UI'), 
            static_folder=os.path.join(BASE_DIR, 'static'))

app.secret_key = "super-secret-key"
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    if 'user' not in session: return redirect(url_for('login_route'))
    return render_template('index.html', **session['user'])

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    if request.method == 'POST':
        # Твоя логика входа
        session['user'] = {'username': 'Miron', 'handle': '@miron', 'avatar': None} 
        return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_route():
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_route'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5555, debug=True)