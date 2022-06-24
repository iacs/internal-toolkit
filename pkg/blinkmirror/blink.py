import requests
from flask import Flask, request

app = Flask(__name__)

BSID = "BS045950-3.0"
CLIENT_HOST = "127.0.0.1"
CLIENT_PORT = "9000"


@app.route("/test")
def test():
    url = f"http://{CLIENT_HOST}:{CLIENT_PORT}/api/v1/test"
    print("***", url)
    res = requests.get(url)
    data = res.json()
    print("***", data)
    return data


@app.route("/color")
def color():
    baseurl = _get_baseurl_v1("set_color")
    payload = request.args
    res = requests.get(baseurl, params=payload)
    data = res.text
    return data


@app.route("/pattern")
def pattern():
    baseurl = _get_baseurl_v1("play_pattern")
    payload = request.args
    res = requests.get(baseurl, params=payload)
    data = res.text
    return data


def _get_baseurl_v1(endpoint):
    return f"http://{CLIENT_HOST}:{CLIENT_PORT}/api/v1/{endpoint}/{BSID}"


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port="5000")
