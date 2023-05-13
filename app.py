# coding=utf8
import logging
import os
import subprocess
import psutil
import datetime
from typing import Any
from flask import Flask, render_template, request

app = Flask(__name__, template_folder="templates")


class Config:
    def __init__(self):
        self.debug = True if os.getenv("DEBUG") == "yes" else False
        self.config_path = os.getenv("CONFIG_PATH", "/config")
        self.dae_bin_path = os.getenv("DAE_BIN_PATH", "/usr/bin/dae")


class Logger:
    def __new__(cls):
        cls._logger = super().__new__(cls)
        logging.root.setLevel(logging.NOTSET)
        cls._logger = logging.getLogger(__name__)
        handler = logging.StreamHandler()
        handler.setLevel(logging.NOTSET)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        cls._logger.addHandler(handler)
        return cls._logger


class UI:
    def __init__(self, config: Config) -> None:
        self.logger = Logger()
        self.selected_theme = "neat"
        self.config = config

    def read_selected_theme(self) -> str:
        return self.selected_theme

    def update_selected_theme(self, theme) -> None:
        self.selected_theme = theme

    def read_config(self) -> Any:
        with open(self.config.config_path, "r") as f:
            config = f.read()
        return config

    def write_config(self, config) -> None:
        with open(self.config.config_path, "w") as f:
            f.write(config)

    def reload_dae(self):
        subprocess.call([self.config.dae_bin_path, "reload"])
        self.logger.info("config reloaded!")

    def start_dae(self):
        cmd = "/usr/bin/systemctl start dae.service"
        result = subprocess.run(cmd.split(), capture_output=True)
        self.logger.warning(result.stdout.decode("utf-8"))
        self.logger.error(result.stderr.decode("utf-8"))

    def stop_dae(self):
        cmd = "/usr/bin/systemctl stop dae.service"
        result = subprocess.run(cmd.split(), capture_output=True)
        self.logger.warning(result.stdout.decode("utf-8"))
        self.logger.error(result.stderr.decode("utf-8"))

    def restart_dae(self):
        cmd = "/usr/bin/systemctl restart dae.service"
        result = subprocess.run(cmd.split(), capture_output=True)
        self.logger.warning(result.stdout.decode("utf-8"))
        self.logger.error(result.stderr.decode("utf-8"))

    def get_dae_runtime(self):
        process_path = "dae"
        for proc in psutil.process_iter(["pid", "create_time", "name"]):
            if proc.name() == process_path:
                create_time = datetime.datetime.fromtimestamp(proc.create_time())
                uptime = datetime.datetime.now() - create_time
                days = uptime.days
                hours, remainder = divmod(uptime.seconds, 3600)
                minutes, seconds = divmod(remainder, 60)
                return [
                    f"{days}days{hours}hour{minutes}minutes{seconds}seconds",
                    "stop",
                    "green",
                ]
        return ["dae not started!", "start", "red"]

    # def update_geodata(self):
    #     subprocess.run(["chmod", "+x", "/root/dae-ui/install-dat-release.sh"])
    #     subprocess.call(["/root/dae-ui/install-dat-release.sh"])
    #     self.reload_dae()


@app.route("/journal")
def journal():
    command = "journalctl -xu dae -n 200 --reverse"
    output = subprocess.check_output(command.split()).decode("utf-8")
    return render_template("journal.html", output=output)


@app.route("/", methods=["GET", "POST"])
def index():
    config = Config()
    ui = UI(config)
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
            ui.start_dae()
        elif action == "Stop":
            ui.stop_dae()
        elif action == "Restart":
            ui.restart_dae()
        elif action == "Reload":
            ui.reload_dae()
        elif action == "Save theme":
            ui.update_selected_theme(select)
        # elif action == "Update geodata":
        #     ui.update_geodata()

        config = ui.read_config()
        select = ui.read_selected_theme()

    return render_template(
        "index.html", config=config, select=select, runtime=ui.get_dae_runtime()
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=Config().debug)
