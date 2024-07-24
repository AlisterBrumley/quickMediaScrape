# BUILT IN IMPORTS
import urllib.error
from dataclasses import dataclass

# DEPENDENCY IMPORTS
import tvdb_v4_official


# contains dictionaries of show info
@dataclass
class SeriesInfo:
    ext: dict
    tra: dict
    eps: dict


# getting authorized access to TVDB database
def auth():
    try:
        return tvdb_v4_official.TVDB("0c337cac-4ac3-4a65-944f-ffcb1eb29a17")
    except urllib.error.URLError as e:
        print("NETWORK ERROR!")
        print(e)
        exit(1)
    except Exception as e:
        print("UNKNOWN ERROR OCCURED:")
        print(e)
        exit(1)


# pulling info from TVDB database
def show_info(db, id):
    try:
        return SeriesInfo(
            db.get_series_extended(id),
            db.get_series_translation(id, "eng"),
            db.get_series_episodes(id, "alternate"),
        )
    except ValueError:
        print("ID incorrect or not correct media type!")
        exit(1)
    except urllib.error.URLError as e:
        print("NETWORK ERROR!")
        print(e)
        exit(1)
    except Exception as e:
        print("UNKNOWN ERROR OCCURED:")
        print(e)
        exit(1)
