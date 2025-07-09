from flask import Flask, request, jsonify
import pandas as pd
import os
app = Flask(__name__)

# Sample data just to simulate
available_metrics = ["gdp_per_capita", "co2_emissions", "literacy_rate"]
available_countries = ["Germany", "India", "Brazil", "USA"]
def load_gdp_data(path):
     
    df = pd.read_csv(path)
    return df
gdp_df = load_gdp_data("data/clean/gdp_cleaned.csv")
sample_data = {
    "Germany": {
        "gdp_per_capita": {2020: 46200, 2021: 48000},
        "co2_emissions": {2020: 7.5, 2021: 7.2},
    },
    "India": {
        "gdp_per_capita": {2020: 2100, 2021: 2300},
        "co2_emissions": {2020: 1.9, 2021: 2.0},
    }
}

@app.route('/')
def home():
    return jsonify({"message": "World Data Explorer backend is running!"})

@app.route('/api/metrics')
def get_metrics():
    return jsonify(available_metrics)

@app.route('/api/countries')
def get_countries():
    return jsonify(available_countries)

@app.route('/api/data')
def get_data():
    metric = request.args.get("metric")
    country = request.args.get("country")
    year = request.args.get("year", type=int)

    if metric != "gdp_per_capita":
        return jsonify({"error": "Only GDP metric supported for now"}), 400

    filtered = gdp_df[
        (gdp_df["Country Name"] == country) &
        (gdp_df["Year"] == year)
    ]

    if filtered.empty:
        return jsonify({"error": "Data not found"}), 404

    value = filtered.iloc[0]["GDP per capita"]
    return jsonify({
        "country": country,
        "metric": metric,
        "year": year,
        "value": value
    })


@app.route('/api/data/comparison')
def compare_data():
    metric = request.args.get("metric")
    countries = request.args.get("countries", "").split(",")
    years = request.args.get("years", "").split(",")
    years = [int(y) for y in years if y.isdigit()]

    result = {}
    for country in countries:
        if country in sample_data and metric in sample_data[country]:
            country_data = sample_data[country][metric]
            filtered = {y: country_data.get(y, None) for y in years} if years else country_data
            result[country] = filtered
        else:
            result[country] = "Metric not found"

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
