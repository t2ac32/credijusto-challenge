from re import L, template
import sys, os, pathlib
from pathlib import Path
import importlib
import flask
from flask import config
from flask import json
import requests as rq
import jwt
import datetime
from enum import Enum
from flask import jsonify, request, make_response, render_template
from flask import session, flash
from functools import wraps
from bs4 import BeautifulSoup

from globals import globals


app = flask.Flask(
    __name__, template_folder="site/templates", static_folder="site/static"
)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "appsecret"
cwd = os.getcwd()

# Create decoratod for token protected routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get(
            "token"
        )  # http://localhost:500/route?token='Theuser generated token'

        if session.get("logged_in"):
            return f(*args, **kwargs)
        if not token:
            return jsonify({"message": "Token is missing!"}), 401

        # verify the token is valid
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"message": "Token is not valid!"}), 401
        return f(*args, **kwargs)

    return decorated


@app.route("/protected")
@token_required
def protected():
    return jsonify({"message": "Route only available with valid tokens."})


@app.route("/")
def login():
    """
    Ask for login authorization to receive a token

    """
    auth = request.authorization

    if auth and auth.password == "appsecret":
        session["logged_in"] = True
        token = jwt.encode(
            {
                "user": auth.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        return render_template("index.html", value=token)
        # return jsonify({"token": token})

    return make_response(
        "Could not verify!", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}
    )


def logout():
    session["logged_in"] = False
    return render_template("404.html")


@app.route("/fixer", methods=["GET"])
@token_required
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
    date = resp.json()["date"]
    value = resp.json()["rates"]["MXN"]
    return {
        "last_updated": date,
        "value": value,
    }


@app.route("/bmx", methods=["GET"])
@token_required
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
    date = resp.json()["bmx"]["series"][0]["datos"][0]["fecha"]
    ex_rate = resp.json()["bmx"]["series"][0]["datos"][0]["dato"]

    return {
        "last_updated": date,
        "value": ex_rate,
    }


@app.route("/dof", methods=["GET"])
@token_required
def dof_USD_MXN():
    """
    Query for latest exchange rate USD TO MXN from Diario oficial de la federacion.

    Parameters:

    Raises:
        ApiError: status code for request
    Returns:
        resp(dictionary): A dictionary containing the json response from API
    """
    URL = globals.DOF_URL
    page = rq.get(URL)

    soup = BeautifulSoup(page.content, "html.parser")
    data_table = soup.find_all("td", class_="b5")

    if len(data_table) == 1:

        data_rows = data_table[0].find_all("tr")
        for row in data_rows:

            if row.get("class") and row.get("class")[0] == "renglonNon":
                # get first cel for each row
                row_cells = row.find_all("td")
                row_date = row_cells[0].text
                fix_val = row_cells[1].text
                dof_val = row_cells[2].text
                pagos_val = row_cells[3].text
                if (
                    all(v is not None for v in [row_date, fix_val, dof_val, pagos_val])
                    is not None
                ):

                    row_date = " ".join(row_date.split())
                    fix_val = " ".join(fix_val.split())
                    dof_val = " ".join(dof_val.split())
                    pagos_val = " ".join(pagos_val.split())

                    dateTime = datetime.datetime.strptime(row_date, "%d/%m/%Y")

                    if dateTime == datetime.datetime.today().replace(
                        second=0, hour=0, minute=0, microsecond=0
                    ):

                        return {
                            "last_updated": dateTime,
                            "value": dof_val,
                        }
    else:
        print("Web format has change and cannot be parsed")

    # get second row of table corresponding to Today date

    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for lates USD to MXN currency exchange rate.</p>"


@app.route("/rates", methods=["GET", "POST"])
def get_rates():
    prov1 = fixer_USD_MXN()
    prov2 = bmx_USD_MXN()
    prov3 = dof_USD_MXN()
    providers = [prov1, prov2, prov3]
    rates = {"rates": {"providers": providers}}
    return rates


@app.route("/submit_provider", methods=["POST"])
def submit_provider():
    if session.get("logged_in"):
        if request.method == "POST":
            if request.form["button"] == "fixer":
                return fixer_USD_MXN()
            elif request.form["button"] == "dof":
                return dof_USD_MXN()
            elif request.form["button"] == "bmx":
                return bmx_USD_MXN()
    else:
        return jsonify({"message": "Session ended, log in to continue!"}), 401


# fixer_USD_MXN()
# bmx_USD_MXN()
# dof_USD_MXN()
if __name__ == "__main__":
    app.run(debug=True)
