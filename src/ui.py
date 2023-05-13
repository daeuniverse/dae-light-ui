import psutil
import datetime
import subprocess
from typing import Any

from logger import logger
from config import Config


class UI:
    def __init__(self, config: Config) -> None:
        self.logger = logger
        self.config = config
        self.selected_theme = "neat"

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
        if result != "":
            self.logger.error(result.stderr.decode("utf-8"))

    def stop_dae(self):
        cmd = "/usr/bin/systemctl stop dae.service"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result != "":
            self.logger.error(result.stderr.decode("utf-8"))

    def restart_dae(self):
        cmd = "/usr/bin/systemctl restart dae.service"
        result = subprocess.run(cmd.split(), capture_output=True)
        if result != "":
            self.logger.error(result.stderr.decode("utf-8"))
        else:
            self.logger.info("dae restarted!")

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
