from flask import Blueprint, request, jsonify, session, redirect, url_for, render_template
from ai.profiler import analyze_portfolio

portfolio_bp = Blueprint('portfolio', __name__)

@portfolio_bp.route('/portfolio', methods=['GET'])
def portfolio():
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    return render_template('portfolio.html', username=session.get('username'))

@portfolio_bp.route('/portfolio/analyze', methods=['POST'])
def analyze():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    holdings = data.get('holdings', [])

    if not holdings:
        return jsonify({'error': 'No holdings provided'}), 400

    result = analyze_portfolio(holdings)
    return jsonify(result), 200