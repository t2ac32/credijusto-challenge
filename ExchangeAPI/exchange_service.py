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
from bs4 import BeautifulSoup

import globals


app = flask.Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = "appsecret"

# Create decoratod for token protected routes
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.args.get(
            "token"
        )  # http://localhost:500/route?token='Theuser generated token'
        if not token:
            return jsonify({"message": "Token is missing!"}), 401
        # verify the token is valid
        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
        except:
            return jsonify({"message": "Token is not valid!"}), 401
        return f(*args, **kwargs)

    return decorated


class Currencies(Enum):
    USD = "USD"
    MXN = "MXN"


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
        token = jwt.encode(
            {
                "user": auth.username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=15),
            },
            app.config["SECRET_KEY"],
            algorithm="HS256",
        )
        print(token)
        return jsonify({"token": token})

    return make_response(
        "Could not verify!", 401, {"WWW-Authenticate": 'Basic realm="Login Required"'}
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


@app.route("/dof", methods=["GET"])
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
                        print("date is today")
                        print(
                            f"fecha: {dateTime} \n",
                            f"fix: {fix_val} \n",
                            f"Diario oficil de la Federacion: {dof_val} \n",
                            f"Pagos: {pagos_val}\n",
                        )
    else:
        print("Web format has change and cannot be parsed")

    # get second row of table corresponding to Today date

    return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for lates USD to MXN currency exchange rate.</p>"


# fixer_USD_MXN()
# bmx_USD_MXN()
dof_USD_MXN()
"""
if __name__ == "__main__":

    app.run(debug=True)
"""
