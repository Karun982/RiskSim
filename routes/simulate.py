from flask import Blueprint, request, jsonify
from simulation.monte_carlo import run_simulation
from simulation.risk_metrics import calculate_metrics
from ai.explainer import explain_portfolio

simulate_bp = Blueprint('simulate', __name__)

@simulate_bp.route('/simulate', methods=['POST'])
def simulate():
    data = request.get_json()

    # --- Validate input ---
    try:
        amount     = float(data.get('amount', 0))
        years      = int(data.get('years', 0))
        asset_type = data.get('asset_type', '')
    except (TypeError, ValueError):
        return jsonify({'error': 'Invalid input types'}), 400

    if amount <= 0:
        return jsonify({'error': 'Amount must be greater than 0'}), 400
    if years <= 0 or years > 50:
        return jsonify({'error': 'Years must be between 1 and 50'}), 400

    VALID_ASSETS = ['stocks', 'mutual_funds', 'crypto', 'bonds', 'gold']
    if asset_type not in VALID_ASSETS:
        return jsonify({'error': f'Asset type must be one of {VALID_ASSETS}'}), 400

    # --- Run simulation ---
    sim_result = run_simulation(amount, years, asset_type, n_simulations=1000)

    # --- Calculate metrics ---
    metrics = calculate_metrics(sim_result['final_values'], amount)

    # --- AI Explanation ---
    ai_explanation = explain_portfolio({
        **metrics,
        'asset_type': asset_type,
        'years': years,
    })
    print("AI:", ai_explanation)

    # --- Build response ---
    response = {
        **metrics,
        'ai_explanation':   ai_explanation,
        'sampled_paths':    sim_result['sampled_paths'],
        'percentile_paths': sim_result['percentile_paths'],
        'labels':           sim_result['labels'],
        'meta':             sim_result['meta'],
    }

    return jsonify(response), 200