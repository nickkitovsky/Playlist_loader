from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.shortcuts import radiolist_dialog
from prompt_toolkit.shortcuts import input_dialog
from local import Config


class Interface:
    def __init__(self, config: Config) -> None:
        self.config = config

    def __draw_radio_dialog(self, title: str, text: str, data: dict[str, str]) -> str:
        result = radiolist_dialog(
            title=title,
            text=text,
            values=[(key, value) for key, value in data.items()],
        ).run()
        return result

    def __draw_checkbox_dialog(self, title: str, text: str, data: list):
        result = checkboxlist_dialog(
            title=title,
            text=text,
            values=data,
        ).run()
        return result

    def select_user(self) -> str:
        title = "Select user"
        text = "Please select user or add new"
        data = {key: key for key in self.config.users.keys()}
        user = self.__draw_radio_dialog(
            title=title, text=text, data=data | {"New User": "newuser"}
        )
        return user

    def select_playlists(self, playlists:list):
        title = "Playlists"
        text = "Select playlists to download"
        data = [
                (
                    entry.get("playlistId"),
                    f'{entry.get("title")} ({entry.get("description")})',
                )
                for entry in playlists
            ]
        playlists = self.__draw_checkbox_dialog(title=title, text = text, data = data)
        return playlists