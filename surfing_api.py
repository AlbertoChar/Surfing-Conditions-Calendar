from flask import Flask, jsonify, render_template
import surfing_conditions

app = Flask(__name__)


@app.route('/surfing-conditions', methods=['GET'])
def surfing_conditions_endpoint():
    conditions = surfing_conditions.get_surfing_conditions()

    times = [entry["Time (GMT+3)"] for entry in conditions]
    wave_heights = [entry["Wave Height (m)"] for entry in conditions]

    return render_template('surfing_conditions.html', times=times, wave_heights=wave_heights, data=conditions)


if __name__ == "__main__":
    app.run(debug=True)
