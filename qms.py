import tvdb_v4_official
import typer
import xml
import xml.etree.ElementTree as ET
import urllib.error
from dataclasses import dataclass
from pathlib import Path
# import pprint


@dataclass
class series_info:
    ext: dict
    tra: dict
    eps: dict


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


def get_info(db, id):
    try:
        show = series_info(
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

    return show


def make_show_xml():
    show_xml = ET.Element("tvshow")
    title = ET.SubElement(show_xml, "title")
    show_title = ET.SubElement(show_xml, "showTitle")
    title.text = "test"

    return show_xml

def main(tvdb_id: str):
    # auth and create class to access database
    tvdb = auth()

    # gets info from database returns in dataclass
    info = get_info(tvdb, tvdb_id)

    # tvshow xml
    xml_tv = make_show_xml()
    
    # PRINTS WITHOUT PRINT!
    ET.dump(xml_tv)

    # pprint.pprint(inf.ext["name"])


if __name__ == "__main__":
    typer.run(main)
