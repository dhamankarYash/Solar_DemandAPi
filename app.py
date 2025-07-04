
from flask import Flask, request, Response, jsonify, render_template
from demand_model import predict_demand
from utils.solar import get_solar_potential, calculate_solar_generation_gwh
from flask_swagger_ui import get_swaggerui_blueprint
from collections import OrderedDict
import pandas as pd
import json

app = Flask(__name__)

# Swagger UI setup
SWAGGER_URL = '/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Demand and Solar Coverage API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict-demand', methods=['GET'])
def predict_demand_route():
    state = request.args.get('state')
    year = request.args.get('year')

    if not state or not year:
        return jsonify({"error": "Missing 'state' or 'year' parameter"}), 400

    try:
        year = int(year)
        prediction = predict_demand(state, year)

        return jsonify({
            "state": state,
            "year": year,
            "predicted_demand_gwh": round(prediction, 2)
        })
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/states', methods=['GET'])
def get_states():
    try:
        df = pd.read_csv('data/final_consumption.csv')
        states = sorted(df['State'].dropna().str.strip().unique())
        return jsonify({"available_states": states})
    except Exception as e:
        return jsonify({"error": f"Failed to read states list: {str(e)}"}), 500


@app.route('/compare', methods=['GET'])
def compare_states():
    state1 = request.args.get('stateA')
    state2 = request.args.get('stateB')
    year = request.args.get('year')

    if not state1 or not state2 or not year:
        return jsonify({"error": "Missing 'stateA', 'stateB' or 'year' parameter"}), 400

    try:
        year = int(year)
        d1 = predict_demand(state1, year)
        d2 = predict_demand(state2, year)

        return jsonify({
            "year": year,
            state1: round(d1, 2),
            state2: round(d2, 2),
            "difference_gwh": round(abs(d1 - d2), 2)
        })
    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/forecast/trend', methods=['GET'])
def forecast_trend():
    state = request.args.get('state')
    if not state:
        return jsonify({"error": "Missing 'state' parameter"}), 400

    try:
        df = pd.read_csv('data/final_consumption.csv')
        df['State'] = df['State'].str.strip()
        state_df = df[df['State'].str.lower() == state.lower()]
        state_df = state_df.sort_values('Year', ascending=False).head(5).sort_values('Year')

        trend = [
            {"year": int(row['Year']), "consumption_gwh": round(row['Consumption'], 2)}
            for _, row in state_df.iterrows()
        ]
        return jsonify({"state": state, "trend": trend})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/demand-vs-solar', methods=['GET'])
def demand_vs_solar():
    state = request.args.get('state')
    year = request.args.get('year')

    if not state or not year:
        return jsonify({"error": "Missing 'state' or 'year' parameter"}), 400

    try:
        year = int(year)
        predicted_demand = predict_demand(state, year)
        solar_potential_mw = get_solar_potential(state)
        solar_generation = calculate_solar_generation_gwh(solar_potential_mw)

        coverage_percent = round((solar_generation / predicted_demand) * 100, 2) if predicted_demand > 0 else 0.0

        if coverage_percent < 20:
            summary = f"Only {coverage_percent}% of {state}'s electricity demand in {year} can be met with solar energy, indicating low solar energy contribution."
        elif coverage_percent < 50:
            summary = f"Around {coverage_percent}% of {state}'s electricity demand in {year} can be fulfilled using solar energy, indicating moderate contribution."
        else:
            summary = f"Over {coverage_percent}% of {state}'s electricity demand in {year} can be fulfilled using solar energy, indicating strong potential for solar-based power generation."

        response = OrderedDict([
            ("year", year),
            ("state", state),
            ("predicted_demand_gwh", round(predicted_demand, 2)),
            ("solar_generation_gwh", round(solar_generation, 2)),
            ("solar_coverage_percent", coverage_percent),
            ("summary", summary)
        ])

        return Response(json.dumps(response), mimetype='application/json')

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)

