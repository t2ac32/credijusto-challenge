import importlib
import flask
from flask import config
from flask import json
import requests as rq
import jwt
import datetime
from enum import Enum
from flask import jsonify, request, make_response
from functools import wraps
import globals


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "secretkey"

# Create decoratod for token protected routes
def token_require(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get(
            "token"
        )  # http://localhost:500/route?token='Theuser generated token'

        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        # verify the token is valid
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"]), 403
        except:
            return jsonify({"message": "Token is not valid!"})
        return f(*args, **kwargs)


class Currencies(Enum):
    USD = "USD"
    MXN = "MXN"


@app.route("/unprotected")
def unprotected():
    return jsonify({"message": "Anyone can view this!"})


@app.route("/protected")
def protected():
    return jsonify({"message": "Route only available with valid tokens"})


@app.route("/")
def login():
    """
    Ask for login authorization to receive a token

    """
    auth = request.authorization

    if auth and auth.password == "pass":
        token = jwt.encode(
            {
                "user": auth.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=15),
            },
            app.config["SECRET_KEY"],
        )

        # return token to the user after successfull log in
        return jsonify({"token": token})

    return make_response(
        "Could not verify!", 401, {"WWW-Authenticate": 'Basic realm="Login Required" '}
    )


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
    # Create query url
    query = (
        globals.BMX_URL
        + globals.BMX_SERIES
        + globals.BMX_USD_MXN_SERIE
        + globals.BMX_LATEST
    )
    # add headers for api request
    headers = {"Bmx-Token": globals.BMX_TOKEN}

    # catch response
    resp = rq.get(query, headers=headers)
    # check for respnse error
    if resp.status_code != 200:
        raise ApiError("GET /tasks/ {}".format(resp.status_code))
    # get exchange rate from reponse json
    ex_rate = resp.json()["bmx"]["series"][0]["datos"][0]["dato"]
    # TODO: Delete unessary print replace for api pretty print
    print(f"BANXICO EXCHANGE RATE: {ex_rate}")
    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for lates USD to MXN currency exchange rate.</p>"


# fixer_USD_MXN()
# bmx_USD_MXN()

if __name__ == "__main__":
    app.run(debug=True)
