# coding: utf-8

# First, you need to import the pulsar module
# Make sure you declare Pulsar as dependency in the addon.xml or it won't work
# You can read it at:
# https://github.com/steeve/plugin.video.pulsar/blob/master/resources/site-packages/pulsar/provider.py
from pulsar import provider
import xbmcaddon

__settings__ = xbmcaddon.Addon(id='script.pulsar.hdbits')
username = __settings__.getSetting('username')
passkey = __settings__.getSetting('passkey')

# Raw search
# query is always a string
def search_string(query):
    return search({"search": query});


# Episode Payload Sample
# {
#     "imdb_id": "tt0092400",
#     "tvdb_id": "76385",
#     "title": "married with children",
#     "season": 1,
#     "episode": 1,
#     "titles": null
# }
def search_episode(episode):
    return search({
        "tvdb": {
            "season": episode["season"],
            "episode": episode["episode"],
        }
    });


# Movie Payload Sample
# Note that "titles" keys are countries, not languages
# The titles are also normalized (accents removed, lower case etc...)
# {
#     "imdb_id": "tt1254207",
#     "title": "big buck bunny",
#     "year": 2008,
#     "titles": {
#         "es": "el gran conejo",
#         "nl": "peach open movie project",
#         "us": "big buck bunny short 2008"
#     }
# }
def search_movie(movie):
    return search({
        "imdb": {
            "id": movie["imdb_id"][2:]
        },
        "medium": [3]
    });

# Make a search through the HDBits API. Format resposne for pulsar
def search(params):
    import json
    import xbmcgui

    params.update({
        "username": username,
        "passkey": passkey
    });

    resp = provider.POST("https://hdbits.org/api/torrents", data=json.dumps(params), headers={"Content-Type": "application/json"}).json()
    if (resp["status"] != 0):
        xbmcgui.Dialog().ok("Something went wrong", json.dumps(resp), json.dumps(params), "")
        return [];

    torrents = resp["data"]

    for torrent in torrents:
        torrent["info_hash"] = torrent["hash"]
        torrent["uri"] = "https://hdbits.org/download.php?passkey=" + passkey + "&id=" + str(torrent["id"])

    return torrents;


# This registers your module for use
provider.register(search_string, search_movie, None)
