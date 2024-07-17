import tvdb_v4_official
import typer
import xml.etree.ElementTree as ET
import urllib.error
from dataclasses import dataclass
from pathlib import Path
import pprint


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


def output_xml(el_tree):
    output = ET.ElementTree(el_tree)
    with open ("tvshow.nfo", "wb") as file:
        output.write(file)


def make_show_xml(inf, show_id, e_len, s_len):
    # TODO find type=2 and maybe language=eng
    thumb_link = inf.ext["artworks"][0]["image"]
    fa_link = inf.ext["artworks"][1]["image"]

    show_xml = ET.Element("tvshow")
    ET.SubElement(show_xml, "title").text = inf.tra["name"]
    ET.SubElement(show_xml, "showtitle").text = inf.ext["aliases"][0]["name"]
    ET.SubElement(show_xml, "originaltitle")  # IGNORE
    uid = ET.SubElement(show_xml, "uniqueid")
    uid.set("default", "true")
    uid.set("type", "tvdb")
    uid.text = show_id
    ET.SubElement(show_xml, "id").text = show_id
    ET.SubElement(show_xml, "ratings")  # IGNORE
    ET.SubElement(show_xml, "userrating").text = "0"
    ET.SubElement(show_xml, "top250").text = "0"
    ET.SubElement(show_xml, "episodes").text = e_len
    ET.SubElement(show_xml, "season").text = s_len
    ET.SubElement(show_xml, "plot").text = inf.tra["overview"]
    ET.SubElement(show_xml, "mpaa").text = inf.ext["contentRatings"][0]["name"]
    ET.SubElement(show_xml, "premeried").text = inf.eps["episodes"][0]["aired"]
    ET.SubElement(show_xml, "dateadded")  # IGNORE
    ET.SubElement(show_xml, "status").text = inf.ext["status"]["name"]
    ET.SubElement(show_xml, "studio").text = inf.ext["companies"][0]["name"]
    ET.SubElement(show_xml, "runtime").text = str(inf.ext["averageRuntime"])
    ET.SubElement(show_xml, "trailer")  # IGNORE
    ET.SubElement(show_xml, "namedseason")  # IGNORE
    ET.SubElement(show_xml, "episodeguide")  # IGNORE
    ET.SubElement(show_xml, "genre") # IGNORE
    thumb = ET.SubElement(show_xml, "thumb") 
    thumb.set("aspect", "poster")
    thumb.set("preview", thumb_link)
    thumb.text = thumb_link
    fa = ET.SubElement(show_xml, "fanart")
    fa.set("preview", fa_link)
    fa.text = fa_link
    ET.SubElement(show_xml, "actor")
    gen = ET.SubElement(show_xml, "generator")
    ET.SubElement(gen, "appname").text = "QuickMediaScraper.py"
    ET.SubElement(gen, "kodiversion").text = "20"
    # ET.SubElement(gen, "datetime").text = TODO ADD DATETIME

    return show_xml

# WIP
def get_files():
    # TODO
    #   SET PATH AS CWD OR MAKE ARG
    #   GLOB MP4's AS WELL
    #   SETUP TO RETURN EPS AND COUNTS
    p = Path("/Users/asta/Movies/temp/Sailor Moon (1995) DIC")
    g = len(sorted(p.glob("S*")))
    r = len(sorted(p.rglob("*.mkv")))
    pprint.pprint(g)
    pprint.pprint(r)


def main(tvdb_id: str):
    # auth and create class to access database
    tvdb = auth()

    # gets info from database returns in dataclass
    info = get_info(tvdb, tvdb_id)

    # todo - get files
    # temp vars
    # get_files()
    seasons = "2"
    episodes = "82"

    # tvshow xml
    xml_tv = make_show_xml(info, tvdb_id, seasons, episodes)

    # writing xml file
    output_xml(xml_tv)

    # PRINTS WITHOUT PRINT!
    # ET.dump(xml_tv)

    # pprint.pprint(inf.ext["name"])


if __name__ == "__main__":
    typer.run(main)
