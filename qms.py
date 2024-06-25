import tvdb_v4_official
import typer
import pprint
import urllib.error
from typing_extensions import Annotated
from typing import Optional


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


def get_info(type, db, id):
    if type == "movie":
        try:
            return db.get_movie(id)
        except ValueError:
            print("ID incorrect or not correct type!")
            exit(1)
        except urllib.error.URLError as e:
            print("NETWORK ERROR!")
            print(e)
            exit(1)
        except Exception as e:
            print("UNKNOWN ERROR OCCURED:")
            print(e)
            exit(1)
    else:
        try:
            return db.get_series(id)
        except ValueError:
            print("ID incorrect or not correct type!")
            exit(1)
        except urllib.error.URLError as e:
            print("NETWORK ERROR!")
            print(e)
            exit(1)
        except Exception as e:
            print("UNKNOWN ERROR OCCURED:")
            print(e)
            exit(1)


def main(
    tvdb_id: str,
    movie: Annotated[Optional[bool], typer.Option("--movie", "-m")] = False,
    series: Annotated[Optional[bool], typer.Option("--series", "-s")] = False
):
    # auth
    tvdb = auth()

    if not movie:
        type = "series"
        print("series")
    else:
        type = "movie"
        print("movie")

    info = get_info(type, tvdb, tvdb_id)
    pprint.pprint(info)


if __name__ == "__main__":
    typer.run(main)
