import os


class Config:
    def __init__(self):
        self.debug = True if os.getenv("DEBUG") == "yes" else False
        self.config_path = os.getenv("CONFIG_PATH", "/config")
        self.dae_bin_path = os.getenv("DAE_BIN_PATH", "/usr/bin/dae")
