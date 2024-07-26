# BUILT IN IMPORTS
import xml.etree.ElementTree as ET
import urllib.request
from pathlib import Path
from dataclasses import dataclass

# DEPENDENCY IMPORTS
import typer

# LOCAL IMPORTS
import helpers.makexml as make
import helpers.dbget as get


@dataclass
class filecounts:
    banner: int = 0
    poster: int = 0
    fanart: int = 0
    clrArt: int = 0
    clrLogo: int = 0
    unknown: int = 0


def output_xml(el_tree, out_path):
    output = ET.ElementTree(el_tree)
    with open(out_path, "wb") as file:
        output.write(file, "UTF-8", True)


def get_files(dir_path):
    return sorted(dir_path.rglob("*.mkv"))


def ep_xml_loop(inf, ep_filelist, act_tree):
    # these vars are the same every ep, so define them here
    show_title = inf.tra["name"]
    mpaa_rating = inf.ext["contentRatings"][0]["name"]
    studio = inf.ext["companies"][0]["name"]

    for cnt, eps in enumerate(ep_filelist):
        ep_inf = inf.eps["episodes"][cnt]
        ep_out_path = eps.with_suffix(".nfo")
        ep_xml = make.episode(inf, ep_inf, show_title, mpaa_rating, studio, act_tree)
        output_xml(ep_xml, ep_out_path)


def art_download(art_inf, series_path):
    # filename counters
    cnt = filecounts()
    series_path = series_path / "images"
    season_cnt = {}  # TODO

    answer = input("Do you want to download artwork(y/N)? ").lower().strip()
    if answer != "y":
        return False

    for art in art_inf:
        match art["type"]:
            case 1:  # banner
                filename = series_path / ("banner-" + str(cnt.banner).zfill(2) + ".jpg")
                cnt.banner += 1
            case 2:  # poster
                filename = series_path / ("poster-" + str(cnt.poster).zfill(2) + ".jpg")
                cnt.poster += 1
            case 3:  # fanart/background
                filename = series_path / ("fanart-" + str(cnt.fanart).zfill(2) + ".jpg")
                cnt.fanart += 1
            case 7:  # season
                continue
            case 22:  # clearart
                filename = series_path / (
                    "clearart-" + str(cnt.clrArt).zfill(2) + ".jpg"
                )
                cnt.clrArt += 1
            case 23:  # clearlogo
                filename = series_path / (
                    "clearlogo-" + str(cnt.clrLogo).zfill(2) + ".jpg"
                )
                cnt.clrLogo += 1
            case _:  # unknown
                filename = series_path / (
                    "UNKNOWN-" + str(cnt.unknown).zfill(2) + ".jpg"
                )
                cnt.unknown += 1
        urllib.request.urlretrieve(art["image"], filename)


def main(tvdb_id: str, dir_path: Path):
    # auth and create var to access database
    tvdb = get.auth()

    # gets info from database, returns in dataclass
    info = get.show_info(tvdb, tvdb_id)

    # making extra info trees
    actor_tree = make.actor(info.ext["characters"])
    art_tree = make.artwork(info.ext["artworks"], info.ext["seasons"])

    # tvshow xml
    series_xml = make.series(info, tvdb_id, actor_tree, art_tree)
    # writing show file
    series_out_path = dir_path / "tvshow.nfo"
    output_xml(series_xml, series_out_path)

    # getting episode files
    episode_filelist = get_files(dir_path)
    # creating and writing episode loop
    ep_xml_loop(info, episode_filelist, actor_tree)

    # asking if user wants to download art
    art_download(info.ext["artworks"], dir_path)


if __name__ == "__main__":
    typer.run(main)
