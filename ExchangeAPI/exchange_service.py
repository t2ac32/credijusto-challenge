import importlib
import flask
import requests as rq
from enum import Enum

import globals

app = flask.Flask(__name__)
app.config["DEBUG"] = True


class Currencies(Enum):
    USD = "USD"
    MXN = "MXN"


@app.route("/fixer", methods=["GET"])
def fixer_USD_MXN():
    """
    Query for lates exchange rate of FIXER USD TO MXN.
    Currently free plan does not allow to change base currency.
    Note: default base currency  = EUR.

    Parameters:

    Raises:
        ApiError: status code for request
    Returns:
        resp(dictionary): A dictionary containing the json response from API
    """
    resp = rq.get(globals.FIXER_URL + globals.ACCES_KEY + globals.USD_MXN)

    if resp.status_code != 200:
        raise ApiError("GET /tasks/ {}".format(resp.status_code))
    print(resp.json())
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for lates USD to MXN currency exchange rate.</p>"


@app.route("/bmx", methods=["GET"])
def bmx_USD_MXN():
    """
    Query for lates exchange rate of BANXICO USD TO MXN.

    Parameters:

    Raises:
        ApiError: status code for request
    Returns:
        resp(dictionary): A dictionary containing the json response from API
    """
    query = (
        globals.BMX_URL
        + globals.BMX_SERIES
        + globals.BMX_USD_MXN_SERIE
        + globals.BMX_LATEST
    )
    print(query)
    headers = {"Bmx-Token": globals.BMX_TOKEN}

    resp = rq.get(query, headers=headers)

    if resp.status_code != 200:
        raise ApiError("GET /tasks/ {}".format(resp.status_code))
    ex_rate = resp.json()["bmx"]["series"][0]["datos"][0]["dato"]

    print(f"BANXICO EXCHANGE RATE: {ex_rate}")
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for lates USD to MXN currency exchange rate.</p>"


# fixer_USD_MXN()
bmx_USD_MXN()
