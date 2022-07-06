from system_oprations import create_dir, Config,  spotdl
from services import YtDiscovery, YandexDiscovery
from interface import UserInterface

config = Config("config.json")
interface = UserInterface(config)

user = interface.change_user_dialog()

if config.users[user] == "ytmusic":
    music_collection = YtDiscovery(username=user)
    music_collection.exctract_playlist()
    playlists = interface.change_playlists(user, music_collection.playlists)
    for playlist in playlists:
        playlist_dirname = playlist[1]
        dirname = create_dir(config=config, directory=[user, playlist_dirname])
        dirname = str(dirname)
        track_list = music_collection.extract_songname(playlist[0])
        for track in track_list:
            spotdl(track_name=track, dir_name=dirname)
elif config.users[user] == "yandex":
    music_collection = YandexDiscovery(username=user)
    # BELOW 'PLAYLISTS' IT'S REALLY BAD SOLUTION (INRFACE CLASS NEEDS REFACTORING)
    playlists = interface.change_playlists(user, playlists=["liked", "daily"])
    for playlist_name in playlists:

        playlist = music_collection.get_playlist(playlist_name)
        playlist_dirname = f"{playlist_name}"
        dirname = create_dir(config=config, directory=[user, playlist_dirname])
        dirname = str(dirname)
        track_list = music_collection.parse_tracks(playlist)
        for track in track_list:
            spotdl(track_name=track, dir_name=dirname)
else: 
    print("new user!")
