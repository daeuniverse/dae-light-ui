# coding=utf8
from flask import Flask, render_template, request
import subprocess
import psutil
import datetime

app = Flask(__name__, template_folder="templates")


@app.route("/journal")
def journal():
    command = "journalctl -xu dae -n 200 --reverse"
    output = subprocess.check_output(command.split()).decode("utf-8")
    return render_template("journal.html", output=output)


def read_select():
    return "neat"


def write_select(select):
    with open("./theme", "w") as f:
        f.write(select)


def read_config():
    with open("config.dae", "r") as f:
        config = f.read()
    return config


def write_config(config):
    with open("config.dae", "w") as f:
        f.write(config)


def start_dae():
    cmd = "/usr/bin/systemctl start dae.service"
    result = subprocess.run(cmd.split(), capture_output=True)

    print(result.stdout.decode("utf-8"))
    print(result.stderr.decode("utf-8"))


def stop_dae():
    cmd = "/usr/bin/systemctl stop dae.service"
    result = subprocess.run(cmd.split(), capture_output=True)

    print(result.stdout.decode("utf-8"))
    print(result.stderr.decode("utf-8"))


def reload_dae():
    subprocess.call(["systemctl", "reload", "dae.service"])


def restart_dae():
    subprocess.call(["/usr/bin/systemctl", "restart", "dae.service"])


def get_dae_runtime():
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


# def update_geodata():
#     subprocess.run(["chmod", "+x", "/root/dae-ui/install-dat-release.sh"])
#     subprocess.call(["/root/dae-ui/install-dat-release.sh"])
#     reload_dae()


@app.route("/", methods=["GET", "POST"])
def index():
    config = read_config()
    select = read_select()
    if request.method == "POST":
        action = request.form["action"]
        config = request.form["config"]
        select = request.form["select"]
        if action == "Save":
            write_config(config)
            reload_dae()
        elif action == "Start":
            start_dae()
        elif action == "Stop":
            stop_dae()
        elif action == "Reload":
            reload_dae()
        elif action == "Restart":
            restart_dae()
        elif action == "Save theme":
            write_select(select)
        # elif action == "Update geodata":
        #     update_geodata()

        config = read_config()
        select = read_select()

    return render_template(
        "index.html", config=config, select=select, runtime=get_dae_runtime()
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
