from types import NoneType
from ytmusicapi import YTMusic
import json
import requests


class YtDiscovery:
    def __init__(self, username: str, **kwargs):
        super().__init__()
        self.username = username
        self.auth()
        self._parse_kwargs(kwargs)

    def _parse_kwargs(self, kwargs: dict):
        good_playlist_name = kwargs.get("good_playlist_name")
        if isinstance(good_playlist_name, NoneType):
            self.__set_default_good_playlist_name()
        elif isinstance(good_playlist_name, tuple or list):
            self.good_playlist_name = good_playlist_name

    def __set_default_good_playlist_name(self):
        self.good_playlist_name = (
            "Mixed for you: moods",
            "Mixed for you",
            "Deep focus",
            "Summer",
            "Recommended radios",
        )

    def auth(self):
        try:
            self._ytmusic = YTMusic(auth=f"auth/{self.username}.json")
        except AttributeError:
            print(
                f"Couldn't open auth/{self.username}.json or file has an incorrect format."
            )
            print("Past request headers from YoutubeMusic service.")
            print(
                "See instruction: https://ytmusicapi.readthedocs.io/en/latest/setup.html"
            )
            self._auth_setup()

    def _auth_setup(self):
        YTMusic.setup(filepath=f"auth/{self.username}.json")
        self.auth()

    def _browse_playlists(self) -> list:
        if self._ytmusic:
            home_content = self._ytmusic.get_home(limit=100)
            return home_content
        else:
            return []

    def exctract_playlist(self):
        home_content = self._browse_playlists()
        if len(home_content) == 0:
            self._auth_setup()
            home_content = self._browse_playlists()
        playlists = []
        for playlist in home_content:
            if self._get_title(playlist) in self.good_playlist_name:
                playlists.extend(playlist.get("contents"))
        self.playlists = playlists

    def extract_songname(self, playlist_id: str):
        tracks = self._get_tracks(playlist_id=playlist_id)
        track_list = [
            f'{" ".join([tr.get("name") for tr in track.get("artists")])} {track.get("title")}'
            for track in tracks
        ]
        return track_list

    def _get_title(self, input_dict_element: dict) -> str:
        if title := input_dict_element.get("title"):
            return title
        else:
            return ""

    def _get_tracks(self, playlist_id: str, limit=100) -> list:
        return self._ytmusic.get_playlist(playlistId=playlist_id, limit=limit)["tracks"]

    # USER INTERACTIVE
    def print_playlists(self, playlists: list):
        print(f"USER: {self.username}")
        print("*" * 80)
        for indx, playlist in enumerate(playlists):
            print(f"{indx}. {playlist.get('title')}:\t{playlist.get('description')}")
        print("*" * 80)

    def change_mix_number(self) -> list[int]:
        print("Select the mixes you need and write them separated by a space: ")
        selected_mixes = input().split(" ")
        return list(map(int, selected_mixes))


class YandexDiscovery:
    def __init__(self, username: str):
        self.username = username
        self.auth()

    def auth(self):
        with open(f"auth/{self.username}.json") as fs:
            self.auth_data = json.loads(fs.read())

    def get_playlist(self, playlist_name: str) -> dict:
        headers = self.auth_data["headers"]
        cookies = self.auth_data["cookies"]
        params = {}
        if playlist_name == "liked":
            params = self.auth_data["params_liked"]
        elif playlist_name == "daily":
            params = self.auth_data["params_daily"]
        #  params=params, cookies=cookies, headers=headers
        response = requests.get(
            "https://music.yandex.ru/handlers/playlist.jsx",
            headers=headers,
            cookies=cookies,
            params=params,
        )
        return response.json()

    def parse_tracks(self, playlist: dict):
        parsed_tracks = []
        tracks = playlist["playlist"]["tracks"]
        for track in tracks:
            # TODO: REMOVE "/ \ *" SYMBOLS
            title = track["title"]
            artists = [artist["name"] for artist in track["artists"]]
            parsed_tracks.append(f"{' '.join(artists)} - {title}")
        return parsed_tracks
