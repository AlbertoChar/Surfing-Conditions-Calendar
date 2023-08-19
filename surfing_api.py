from flask import Flask, jsonify
import main  # Replace with the name of your main module

app = Flask(__name__)


class SurfingAPI:

    def __init__(self):
        pass

    @staticmethod
    @app.route('/surfing-conditions', methods=['GET'])
    def surfing_conditions_endpoint():
        conditions = main.get_surfing_conditions()
        return jsonify(conditions)

    def run(self):
        app.run(debug=True)


if __name__ == "__main__":
    api = SurfingAPI()
    api.run()
