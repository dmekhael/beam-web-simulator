from flask import Flask, render_template, request
from beam import Beam
import numpy as np
import matplotlib.pyplot as plt
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    graph_url = None
    explanation = None
    selected_load = "point"  # default

    if request.method == "POST":
        length = float(request.form["length"])
        load = float(request.form["load"])
        E = float(request.form["E"])
        I = float(request.form["I"])
        load_type = request.form["load_type"]
        selected_load = load_type

        x = np.linspace(0, length, 500)

        # Deflection logic
        if load_type == "point":
            y = (load * x * (length**3 - 2*length*x**2 + x**3)) / (6 * E * I * length)
            explanation = "This is the deflection of a simply supported beam with a center point load."
        elif load_type == "uniform":
            y = (5 * load * x**4) / (384 * E * I)
            explanation = "This is a beam under a uniformly distributed load."
        elif load_type == "moment":
            y = (load * x**2) / (2 * E * I)
            explanation = "This simulates a beam with a moment applied at one end."
        else:
            y = np.zeros_like(x)
            explanation = "Invalid load type."

        # Save graph
        if not os.path.exists("static"):
            os.makedirs("static")

        filename = f"static/{uuid.uuid4().hex}.png"
        plt.figure()
        plt.plot(x, y, color="#00f", label="Deflection")
        plt.plot(x, np.zeros_like(x), 'k--', label="Original Beam")
        plt.xlabel("Beam Length (m)")
        plt.ylabel("Deflection (m)")
        plt.title("Beam Deflection Curve")
        plt.legend()
        plt.grid(True)
        plt.savefig(filename)
        plt.close()

        graph_url = filename.replace("static/", "")

    return render_template("index.html", graph_url=graph_url, explanation=explanation, selected_load=selected_load)

if __name__ == "__main__":
    app.run(debug=True)
