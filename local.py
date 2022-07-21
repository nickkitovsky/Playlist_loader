from pathlib import Path
from datetime import date
import subprocess
import json
import os


class Config:
    def __init__(self, config_file: str = "config.json"):
        self.__SERVICES = ("ytmusic", "yandex")
        self.config_file = config_file
        self.read_config()

    def read_config(self):
        try:
            with open(self.config_file) as fs:
                rawconfig = json.load(fs)
        except FileNotFoundError:
            print(f"Config file: {self.config_file} not found.")
        else:
            self.__parse_config(rawconfig)

    def __parse_config(self, rawconfig: dict):
        if music_dir := rawconfig.get("music_dir"):
            if not Path(music_dir).exists():
                try:
                    Path(music_dir).mkdir(parents=True, exist_ok=True)
                except FileNotFoundError:
                    print(f"Error '{music_dir=}' value")
            self.music_dir = music_dir
        else:
            print(
                f"Error open 'music_dir' value in config\nPlease edit {self.config_file}."
            )
        if users := rawconfig.get("users"):
            self.users = {}
            for username, service in users.items():
                if (
                    service in self.__SERVICES
                    and Path(f"auth/{username}.json").is_file()
                ):
                    self.users.update({username: service})

    def add_user(self, userdata: dict[str, str]):
        self.users.update(userdata)

    def write_config(self):
        config = {}
        config.update({"music_dir": self.music_dir})
        config.update({"users": self.users})
        with open(self.config_file, mode="w") as fs:
            try:
                fs.write(json.dumps(config))
            except FileNotFoundError:
                print(f"Error write config to {self.config_file}")




def create_dir(config: Config, directory: list | tuple):

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
