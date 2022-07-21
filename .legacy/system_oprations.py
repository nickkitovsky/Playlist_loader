from pathlib import Path
from datetime import date
import subprocess
import json
import os


class Config:
    def __init__(self, config_file: str = "config.json"):
        self.config_file = config_file
        self.read_config()
        if self.rawconfig:
            self.music_dir = self.rawconfig.get("music_dir")
            self.users = self.rawconfig.get("users")
        else:
            print("Error config file.")

    def read_config(self):
        try:
            with open(self.config_file) as fs:
                self.rawconfig = json.load(fs)
        except FileNotFoundError:
            print(f"Config file: {self.config_file} not found.")
            self.rawconfig = None


    
def create_dir(config: Config, directory: list| tuple):

    if config:
        music_dir = str(config.music_dir)
    else:
        raise FileNotFoundError("Error load config file.")
    calendardate = date.today().strftime("%d_%m_%Y")
    datestamp = calendardate
    # week_number = date.today().strftime("%U")
    # datestamp = week_number
    current_path = Path(music_dir)
    newpath = Path(current_path / datestamp / f"/".join(directory))
    newpath.mkdir(parents=True, exist_ok=True)
    return newpath

def spotdl_win(track_name: str, dir_name: str):
    p = subprocess.run(["spotdl_loader.bat", track_name, dir_name])


def spotdl_linux(track_name: str, dir_name: str):
    pass


if os.name == "nt":
    spotdl = spotdl_win
# ADD LINUX
elif os.name == "posix":
    spotdl = spotdl_linux
