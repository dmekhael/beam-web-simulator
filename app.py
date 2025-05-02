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
    if request.method == "POST":
        length = float(request.form["length"])
        load = float(request.form["load"])
        E = float(request.form["E"])
        I = float(request.form["I"])

        beam = Beam(length, load, E, I)
        x = np.linspace(0, length, 100)
        y = beam.deflection(x)

        # Save to static/
        if not os.path.exists("static"):
            os.makedirs("static")

        filename = f"static/{uuid.uuid4().hex}.png"
        plt.figure()
        plt.plot(x, y, label="Deflection Curve", color="#00f")
        plt.xlabel("Length (m)")
        plt.ylabel("Deflection (m)")
        plt.title("Beam Deflection")
        plt.grid(True)
        plt.legend()
        plt.savefig(filename)
        plt.close()

        # For use in <img src="{{ graph_url }}">
        graph_url = filename.replace("static/", "")

    return render_template("index.html", graph_url=graph_url)

if __name__ == "__main__":
    app.run(debug=True)
