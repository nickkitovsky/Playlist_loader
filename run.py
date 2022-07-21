from local import Config
from interface import Interface
from services import YoutubeMusic

config = Config()
ui = Interface(config)
user = ui.select_user()
my_service = YoutubeMusic(username=user)
my_service.get_playlists()
selected_playlists_id = ui.select_playlists(my_service.all_playlists)
my_service.add_favorite_playlists(selected_playlists_id)
my_service.prepare_to_download()