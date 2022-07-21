from ytmusicapi import YTMusic


class YoutubeMusic:
    """This class a wrapper around 'ytmusicapi' for getting the personal playlists
    You can to define 'good_playlist_name' value in __init__ function.
    Default values: "Mixed for you: moods", "Mixed for you", "Deep focus", "Summer", "Recommended radios"
    """

    def __init__(self, username: str, **kwargs) -> None:
        super().__init__()
        self.username = username
        self.is_auth = False
        self.auth()
        self._parse_kwargs(kwargs)

    def _parse_kwargs(self, kwargs: dict) -> None:
        good_playlist_name = kwargs.get("good_playlist_name")
        if isinstance(good_playlist_name, type(None)):
            self.__set_default_good_playlist_name()
        elif isinstance(good_playlist_name, tuple or list):
            self.good_playlist_name = good_playlist_name

    def __set_default_good_playlist_name(self) -> None:
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
        self._check_auth()

    def _auth_setup(self):
        YTMusic.setup(filepath=f"auth/{self.username}.json")
        self.auth()

    def _check_auth(self):
        try:
            self._ytmusic.get_liked_songs(limit=1)

        except Exception:
            print(
                f"Auth error. please put headers again.\nSee instruction: https://ytmusicapi.readthedocs.io/en/latest/setup.html"
            )
            self._auth_setup()
        else:
            self.is_auth = True

    def get_playlists(self, parse_result: bool = True):
        if self.is_auth:
            home_content = self._ytmusic.get_home(limit=100)
        else:
            self.auth()
            home_content = self._ytmusic.get_home(limit=100)
        playlists = []
        for playlist in home_content:
            if self._get_title(playlist) in self.good_playlist_name:
                playlists.extend(playlist["contents"])
        if parse_result:
            self.all_playlists = self._parse_playlists(playlists=playlists)
        else:
            self.all_playlists = playlists

    def _parse_playlists(self, playlists: list) -> list:
        parsed_result = [
            {
                "title": playlist.get("title"),
                "playlistId": playlist.get("playlistId"),
                "description": playlist.get("description"),
            }
            for playlist in playlists
        ]
        return parsed_result

    def add_favorite_playlists(self, playlists_id: list):
        self.favorite_playlists = [
            favorite
            for favorite in self.all_playlists
            if favorite.get("playlistId") in playlists_id
        ]

    def _get_title(self, input_dict_element: dict) -> str:
        if title := input_dict_element.get("title"):
            return title
        else:
            return ""

    def get_tracks(self, playlist_id: str, limit=100, parse_result=True) -> list:
        tracks = self._ytmusic.get_playlist(playlistId=playlist_id, limit=limit)[
            "tracks"
        ]
        if parse_result:
            return self._parse_tracks(tracks)
        else:
            return tracks

    def _parse_tracks(self, tracks: list) -> list:
        track_list = [
            f'{" ".join([tr.get("name") for tr in track.get("artists")])} {track.get("title")}'
            for track in tracks
        ]
        return track_list

    def prepare_to_download(self):
        self.complete_result = []
        for playlist in self.favorite_playlists:
            dirname = f'{playlist.get("title")} • {playlist.get("description")}'
            tracks = self.get_tracks(playlist_id=playlist.get("playlistId"))
            self.complete_result.append({"dirname": dirname, "tracks": tracks})

    # def new_user(self):
    #     pass
    # # USER INTERACTIVE
    # def print_playlists(self, playlists: list):
    #     print(f"USER: {self.username}")
    #     print("*" * 80)
    #     for indx, playlist in enumerate(playlists):
    #         print(f"{indx}. {playlist.get('title')}:\t{playlist.get('description')}")
    #     print("*" * 80)

    # def change_mix_number(self) -> list[int]:
    #     print("Select the mixes you need and write them separated by a space: ")
    #     selected_mixes = input().split(" ")
    #     return list(map(int, selected_mixes))
