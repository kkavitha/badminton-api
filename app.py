from flask import Flask, jsonify
from flask_cors import CORS

from find_court_on_date import get_locations

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/locations")
def main():
    locations = get_locations()
    json = {"locations": locations}
    return jsonify(json)


if __name__ == "__main__":
    app.run()
