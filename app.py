from flask import Flask, jsonify

from find_court_on_date import get_locations

app = Flask(__name__)


@app.route("/locations")
def main():
    return jsonify(get_locations())


if __name__ == "__main__":
    app.run()
