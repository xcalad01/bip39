import requests
import os

from requests.adapters import HTTPAdapter, Retry
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})
app.config['CORS_HEADERS'] = 'Content-Type'

retries = Retry(total=5,
                backoff_factor=0.1,
                status_forcelist=[ 500, 502, 503, 504 ])

CHECK_ADDRESS_SESSION = requests.Session()
CHECK_ADDRESS_SESSION.mount('https://', HTTPAdapter(max_retries=retries))

TRANSACTIONS_INFO_SESSION = requests.Session()
TRANSACTIONS_INFO_SESSION.mount('https://', HTTPAdapter(max_retries=retries))


TREZOR_URLS_BY_TOKENS = {
    "BTC": os.environ.get("TREZOR_URL_BTC", "https://btc2.trezor.io/api/v2/"),
    "ETH": os.environ.get("TREZOR_URL_ETH", "https://eth2.trezor.io/api/v2/"),
    "DOGE": os.environ.get("TREZOR_URL_DOGE", "https://doge2.trezor.io/api/v2/"),
    "BCH": os.environ.get("TREZOR_URL_BCH", "https://bch2.trezor.io/api/v2/"),
    "BTG": os.environ.get("TREZOR_URL_BTG", "https://btg2.trezor.io/api/v2/"),
    "LTC": os.environ.get("TREZOR_URL_LTC", "https://ltc2.trezor.io/api/v2/"),
    "DGB": os.environ.get("TREZOR_URL_DGB", "https://dgb2.trezor.io/api/v2/"),
}

@app.route("/ping")
def ping():
    return jsonify({"pong": True})


@app.route("/check_address")
def check_address():
    token = request.args.get("token")
    if not token:
        return jsonify({"message": "token not specified"}), 401
    if token not in TREZOR_URLS_BY_TOKENS:
        return jsonify({"message": "unsupported token"}), 401

    address = request.args.get("address")
    if not address:
        return jsonify({"message": "address not specified"}), 401

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:99.0) Gecko/20100101 Firefox/99.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    }

    r = CHECK_ADDRESS_SESSION.get(TREZOR_URLS_BY_TOKENS[token] + f"address/{address}", headers=headers)
    if r.status_code == 200:
        return jsonify(r.json()), 200
    else:
        return jsonify({}), 401


if __name__ == "__main__":
    app.run("0.0.0.0", port=8001)
