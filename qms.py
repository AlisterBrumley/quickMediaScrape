import tvdb_v4_official
import typer
import pprint
import urllib.error
# from typing_extensions import Annotated
# from typing import Optional


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


# def get_info_DISABLE(mov, db, id, season):
#     if mov:
#         try:
#             return db.get_movie(id)
#         except ValueError:
#             print("ID incorrect or not correct media type!")
#             exit(1)
#         except urllib.error.URLError as e:
#             print("NETWORK ERROR!")
#             print(e)
#             exit(1)
#         except Exception as e:
#             print("UNKNOWN ERROR OCCURED:")
#             print(e)
#             exit(1)
#     else:  # if not movie, is series
#         try:
#             return db.get_series(id)
#         except ValueError:
#             print("ID incorrect or not correct media type!")
#             exit(1)
#         except urllib.error.URLError as e:
#             print("NETWORK ERROR!")
#             print(e)
#             exit(1)
#         except Exception as e:
#             print("UNKNOWN ERROR OCCURED:")
#             print(e)
#             exit(1)


def get_info(db, id):
    try:
        # TODO RETURN MULTIPLE DICTS
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


def get_season_type(db, id):
    try:
        s_types = db.get_series_extended(id)["seasonTypes"]
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

    list_print(s_types)

    list_length = len(s_types)
    selection = select(list_length)
    return s_types[selection]["type"]


# prints season type list
def list_print(list):
    for cnt, dct in enumerate(list):
        cnt = str(cnt).zfill(2)
        s_name = dct["name"]
        s_type = dct["type"]

        print(cnt + ") " + s_name + " - " + s_type)


# user selection
def select(lst_len):
    selection = input("Selection: ")

    # if no input try again
    if not selection:
        return select(lst_len)
    # if not int try again
    try:
        selection = int(selection)
    except ValueError:
        return select(lst_len)
    # if out of range try again
    if int(selection) >= lst_len:
        return select(lst_len)

    return selection


# MOVIES DISABLED FOR TIME BEING
def main(
    tvdb_id: str,
    # movie: Annotated[Optional[bool], typer.Option("--movie", "-m")] = False,
    # series: Annotated[Optional[bool], typer.Option("--series", "-s")] = False
):
    # auth and create class to access database
    tvdb = auth()

    # getting season types and selecting one
    # if not movie:
    #     season_type = get_season_type(tvdb, tvdb_id)
    # else:
    #     season_type = None

    # getting info, curently not using season type, check notes
    # info = get_info_DISABLE(movie, tvdb, tvdb_id, season_type)
    # TODO GET MULTIPLE DICTS
    info = get_info(tvdb, tvdb_id)

    # TODO CREATE CLASSES FROM DICTS

    # TODO CREATE XML FROM CLASSES

    pprint.pprint(info)


if __name__ == "__main__":
    typer.run(main)
