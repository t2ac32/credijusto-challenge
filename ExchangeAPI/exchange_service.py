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


@app.route("/", methods=["GET"])
def fixer_USD_MXN():
    # Query for lates exchange rate of FIXER USD TO MXN
    # Currently free plan don't allow to change base currency
    # Default base currency  = EUR
    resp = rq.get(globals.FIXER_URL + globals.ACCES_KEY + globals.USD_MXN)

    if resp.status_code != 200:
        raise ApiError("GET /tasks/ {}".format(resp.status_code))
    print(resp.json())
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for lates USD to MXN currency exchange rate.</p>"
