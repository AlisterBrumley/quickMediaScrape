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


def get_info(mov, db, id):
    if mov:
        try:
            return db.get_movie(id)
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
    else:  # if not movie, is series
        try:
            return db.get_series(id)
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


def main(
    tvdb_id: str,
    movie: Annotated[Optional[bool], typer.Option("--movie", "-m")] = False,
    # VVV disabled, due to being default and unncesary
    # series: Annotated[Optional[bool], typer.Option("--series", "-s")] = False
):
    # auth and create class to access database
    tvdb = auth()

    info = get_info(movie, tvdb, tvdb_id)
    pprint.pprint(info)


if __name__ == "__main__":
    typer.run(main)
