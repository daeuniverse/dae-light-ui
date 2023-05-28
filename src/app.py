# coding=utf8
import subprocess

from flask import Flask, render_template, request

from config import Config
from ui import UI

app = Flask(__name__)

config = Config()
ui = UI(config)


@app.route("/logs")
def journal():
    command = "journalctl -xu dae -n 200 --reverse"
    output = subprocess.check_output(command.split()).decode("utf-8")
    return render_template("journal.html", output=output)


@app.route("/", methods=["GET", "POST"])
def index():
    config = ui.read_config()
    select = ui.read_selected_theme()
    if request.method == "POST":
        action = request.form["action"]
        config = request.form["config"]
        select = request.form["select"]
        if action == "Save":
            ui.write_config(config)
            ui.reload_dae()
        elif action == "Start":
            ui.update_dae_state("start")
        elif action == "Stop":
            ui.update_dae_state("stop")
        elif action == "Restart":
            ui.update_dae_state("restart")
        elif action == "Save theme":
            ui.update_selected_theme(select)
        # elif action == "Update geodata":
        #     ui.update_geodata()

        config = ui.read_config()
        select = ui.read_selected_theme()

    return render_template(
        "index.html",
        config=config,
        select=select,
        runtime=ui.get_dae_runtime(),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config().debug)
