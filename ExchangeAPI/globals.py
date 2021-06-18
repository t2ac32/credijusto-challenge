import importlib


# DOF_URL =
# BANXICO_URL =


"""""" """
Fixer
""" """"""
FIXER_URL = "http://data.fixer.io/api/"
API_KEY = "c55e6d60de6f4f5e2014186b2f58fb43"
# FIXER PATHS
ACCES_KEY = f"latest?access_key={API_KEY}"
USD_MXN = "&symbols=MXN,USD"
MXN_USD = "&base=MXN&symbols=USD"

"""""" """
Banxico 
""" """"""
BMX_URL = "https://www.banxico.org.mx/SieAPIRest/service/v1/"
BMX_TOKEN = "691ad5611a5cb5041f9c5203da920c32ff1f207c3d58dbad1b3d8146af372829"
BMX_QUERY = f"token={BMX_TOKEN}"

# Banxico PATHS
BMX_SERIES = "series/"
BMX_LATEST = "//datos/oportuno"
# BANXICO SERIES
BMX_USD_MXN_SERIE = "SF43718"
BMX_EUR_SERIE = "SF46410"
BMX_CUSD_SERIE = "SF60632"
BMX_JPY_SERIE = "SF46406"
BMX_GBP_SERIE = "SF46407"
