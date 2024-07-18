import tvdb_v4_official
import typer
import xml.etree.ElementTree as ET
import urllib.error
from dataclasses import dataclass
from pathlib import Path


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


def len_seasons(s_list):
    alt = "alternate"
    return sum(seasons["type"]["type"] == alt for seasons in s_list)


def output_xml(el_tree, out_path):
    output = ET.ElementTree(el_tree)
    with open(out_path, "wb") as file:
        output.write(file, "UTF-8", True)


def make_series_xml(inf, show_id):
    # TODO find type=n and maybe language=eng for art links
    thumb_link = inf.ext["artworks"][0]["image"]
    fa_link = inf.ext["artworks"][1]["image"]
    ep_len = str(len(inf.eps["episodes"]))
    sea_len = str(len_seasons(inf.ext["seasons"]))

    # setting root of xml
    show_xml = ET.Element("tvshow")

    # setting values of xml
    ET.SubElement(show_xml, "title").text = inf.tra["name"]
    ET.SubElement(show_xml, "showtitle").text = inf.ext["aliases"][0]["name"]
    ET.SubElement(show_xml, "originaltitle").text = inf.ext["name"]
    uid = ET.SubElement(show_xml, "uniqueid")
    uid.set("default", "true")
    uid.set("type", "tvdb")
    uid.text = show_id
    ET.SubElement(show_xml, "id").text = show_id
    ET.SubElement(show_xml, "ratings")  # IGNORE
    ET.SubElement(show_xml, "userrating").text = "0"
    ET.SubElement(show_xml, "top250").text = "0"
    ET.SubElement(show_xml, "episodes").text = ep_len
    ET.SubElement(show_xml, "season").text = sea_len
    ET.SubElement(show_xml, "plot").text = inf.tra["overview"]
    ET.SubElement(show_xml, "mpaa").text = inf.ext["contentRatings"][0]["name"]
    ET.SubElement(show_xml, "premiered").text = inf.eps["episodes"][0]["aired"]
    ET.SubElement(show_xml, "dateadded")  # IGNORE
    ET.SubElement(show_xml, "status").text = inf.ext["status"]["name"]
    ET.SubElement(show_xml, "studio").text = inf.ext["companies"][0]["name"]
    ET.SubElement(show_xml, "runtime").text = str(inf.ext["averageRuntime"])
    ET.SubElement(show_xml, "trailer")  # IGNORE
    ET.SubElement(show_xml, "namedseason")  # IGNORE
    ET.SubElement(show_xml, "episodeguide")  # IGNORE
    ET.SubElement(show_xml, "genre")  # IGNORE
    thumb = ET.SubElement(show_xml, "thumb")
    thumb.set("aspect", "poster")
    thumb.set("preview", thumb_link)
    thumb.text = thumb_link
    # fanart doesnt work; TODO download artworks
    fa = ET.SubElement(show_xml, "fanart")
    fa_thumb = ET.SubElement(fa, "thumb")
    fa_thumb.set("preview", fa_link)
    fa_thumb.text = fa_link
    ET.SubElement(show_xml, "actor")  # IGNORE FOR NOW
    gen = ET.SubElement(show_xml, "generator")
    ET.SubElement(gen, "appname").text = "QuickMediaScraper.py"
    ET.SubElement(gen, "kodiversion").text = "20"
    # ET.SubElement(gen, "datetime").text = TODO ADD DATETIME

    # adding indents
    ET.indent(show_xml, " ", 4)

    return show_xml


def make_episode_xml(inf):
    ep_xml = ET.Element("episodedetails")


def get_files(dir_path):
    return sorted(dir_path.rglob("*.mkv"))


def main(tvdb_id: str, dir_path: Path):
    # auth and create var to access database
    tvdb = auth()

    # gets info from database, returns in dataclass
    info = get_info(tvdb, tvdb_id)

    # tvshow xml
    series_xml = make_series_xml(info, tvdb_id)
    # writing show file
    series_out_path = dir_path / "tvshow.nfo"
    output_xml(series_xml, series_out_path)

    # getting episode files
    ep_filelist = get_files(dir_path)
    for eps in ep_filelist:
        ep_out_path = eps.with_suffix(".nfo")
        ep_xml = make_episode_xml(info)
        # output_xml(ep_xml, ep_out_path)


if __name__ == "__main__":
    typer.run(main)
