from prompt_toolkit.shortcuts import checkboxlist_dialog
from prompt_toolkit.shortcuts import radiolist_dialog
from system_oprations import Config


class UserInterface:
    def __init__(self, config: Config) -> None:
        self.config = config

    def change_user_dialog(self):
        users = list(self.config.users.keys()) + [
            "new_user",
        ]
        result = radiolist_dialog(
            title="Users",
            text="Select the desired user",
            values=[(f"{user}", user) for user in users],
        ).run()
        if result in users:
            return result
        else:
            return self.new_user()

    def new_user(self):
        print("new_user()")
        return "SHABLODA!!!"

    def playlist_template(self, user, playlists):
        if self.config.users[user] == "ytmusic":
            return [
                (
                    (pl["playlistId"], f"{pl['title']} • {pl['description']}"),
                    f"{pl['title']} • {pl['description']}",
                )
                for pl in playlists
            ]
        elif self.config.users[user] == "yandex":
            return [("liked", "Liked Playlist"), ("daily","Daily Playlist")]

    def change_playlists(self, user: str, playlists: list):
        results_array = checkboxlist_dialog(
            title="Playlists",
            text="Check playlist to download",
            values=self.playlist_template(user, playlists),
        ).run()
        return results_array
