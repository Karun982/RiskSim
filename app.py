from flask import Flask, session, redirect, url_for, render_template
from routes.simulate import simulate_bp
from routes.auth import auth_bp
from routes.portfolio import portfolio_bp


app = Flask(__name__)
app.secret_key = 'risksim-secret-2026'

app.register_blueprint(simulate_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(portfolio_bp)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/app')
def app_home():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    return render_template('form.html', username=session.get('username'))

@app.route('/result')
def result():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    return render_template('result.html', username=session.get('username'))


if __name__ == '__main__':
    app.run(debug=True)