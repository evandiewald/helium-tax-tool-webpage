from flask import Flask, jsonify, request, make_response, render_template, redirect, url_for, flash, session, render_template_string
from flask_bootstrap import Bootstrap
from forms import *
from utils import *
import pandas as pd

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'secret'


@app.route('/', methods=["GET", "POST"])
def home():
    addressForm = AccountForm()
    hotspotForm = HotspotForm()
    if addressForm.submit_account.data and addressForm.validate_on_submit():
        df, total_taxable_income_usd = export_helium_taxes(addressForm.address.data)
        # df = pd.read_csv('coingecko_prices_2020.csv')
        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=account_earnings_2020.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    if hotspotForm.submit_hotspot.data and hotspotForm.validate_on_submit():
        print(hotspotForm.address.data)
        df, total_taxable_income_usd = export_hotspot_taxes(hotspotForm.address.data)
        # df = pd.read_csv('coingecko_prices_2020.csv')
        resp = make_response(df.to_csv())
        resp.headers["Content-Disposition"] = "attachment; filename=hotspot_earnings_2020.csv"
        resp.headers["Content-Type"] = "text/csv"
        return resp
    return render_template("index.html", addressForm=addressForm, hotspotForm=hotspotForm)


@app.route('/account/', methods=["GET"])
def export_account():
    if request.method == "GET":
        try:
            address = request.args.get('address')
            df, total_taxable_income_usd = export_helium_taxes(address)
            # df = pd.read_csv('coingecko_prices_2020.csv')
            resp = make_response(df.to_csv())
            resp.headers["Content-Disposition"] = "attachment; filename=account_earnings_2020.csv"
            resp.headers["Content-Type"] = "text/csv"
        except ValueError:
            resp = """Wallet not found. Make sure you're using a valid HNT Wallet Address that owns hotspots. If exporting earnings for an individual hotspot, use the "Export by Hotspot" tab."""
        return resp


@app.route('/hotspot/', methods=["GET"])
def export_hotspot():
    if request.method == "GET":
        try:
            address = request.args.get('hotspot')
            df, total_taxable_income_usd = export_hotspot_taxes(address)
            # df = pd.read_csv('coingecko_prices_2020.csv')
            resp = make_response(df.to_csv())
            resp.headers["Content-Disposition"] = "attachment; filename=hotspot_earnings_2020.csv"
            resp.headers["Content-Type"] = "text/csv"
        except ValueError:
            resp = """Hotspot not found. Make sure you're using a valid hotspot address. If exporting earnings for all hotspots in a given HNT wallet, use the "Export by Account" tab."""
        return resp


if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True)