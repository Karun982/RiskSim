from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if session.get('logged_in'):
            return redirect(url_for('index'))
        return render_template('login.html')

    data = request.get_json() or request.form
    username = data.get('username', '').strip().lower()
    password = data.get('password', '').strip()

    if username and password:
        session['logged_in'] = True
        session['username'] = username
        return jsonify({'success': True, 'redirect': url_for('index')}), 200
    else:
        return jsonify({'success': False, 'error': 'Please enter username and password'}), 401

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))