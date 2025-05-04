from flask import Flask, render_template, request
from beam_model import Beam
import numpy as np
import matplotlib.pyplot as plt
import os
import uuid

app = Flask(__name__)

def save_plot(x, y, ylabel, title, filename, color):
    plt.figure()
    plt.plot(x, y, label=title, color=color)
    plt.axhline(0, linestyle='--', color='gray')
    plt.xlabel("Position (m)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

@app.route("/", methods=["GET", "POST"])
def index():
    graph_url = None
    moment_url = None
    shear_url = None
    explanation = None
    formula = ""
    selected_load = "point"

    if request.method == "POST":
        length = float(request.form["length"])
        load = float(request.form["load"])
        E = float(request.form["E"])
        I = float(request.form["I"])
        load_type = request.form["load_type"]
        selected_load = load_type

        beam = Beam(length, load, E, I, load_type)
        result = beam.max_deflection()
        formula = beam.formula()
        explanation = beam.explanation()

        x = np.linspace(0, length, 500)

        # Calculate deflection
        if load_type == "point":
            y_deflect = (load * x * (length**3 - 2 * length * x**2 + x**3)) / (6 * E * I * length)
        elif load_type == "uniform":
            y_deflect = (5 * load * x**4) / (384 * E * I)
        elif load_type == "moment":
            y_deflect = (load * x**2) / (2 * E * I)
        else:
            y_deflect = np.zeros_like(x)

        # Moment and shear
        y_moment = beam.moment_array(x)
        y_shear = beam.shear_array(x)

        # Delete old plots
        for file in os.listdir("static"):
            if file.endswith(".png"):
                os.remove(os.path.join("static", file))

        # Save deflection graph
        deflect_file = f"static/{uuid.uuid4().hex}_deflect.png"
        save_plot(x, y_deflect, "Deflection (m)", "Beam Deflection Curve", deflect_file, "blue")
        graph_url = deflect_file.replace("static/", "")

        # Save moment graph
        moment_file = f"static/{uuid.uuid4().hex}_moment.png"
        save_plot(x, y_moment, "Moment (Nm)", "Bending Moment Diagram", moment_file, "orange")
        moment_url = moment_file.replace("static/", "")

        # Save shear graph
        shear_file = f"static/{uuid.uuid4().hex}_shear.png"
        save_plot(x, y_shear, "Shear Force (N)", "Shear Force Diagram", shear_file, "green")
        shear_url = shear_file.replace("static/", "")

        return render_template("index.html",
                               result=result,
                               formula=formula,
                               explanation=explanation,
                               graph_url=graph_url,
                               moment_url=moment_url,
                               shear_url=shear_url,
                               selected_load=selected_load,
                               beam_length=length)

    return render_template("index.html", selected_load=selected_load)

if __name__ == "__main__":
    app.run(debug=True)
