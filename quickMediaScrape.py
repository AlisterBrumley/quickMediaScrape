# BUILT IN IMPORTS
from pathlib import Path

# DEPENDENCY IMPORTS
import typer

# LOCAL IMPORTS
import helpers.xml_tools as xml_t
import helpers.database_tools as get_db
import helpers.download_tools as dt


def get_files(dir_path):
    return sorted(dir_path.rglob("*.mkv"))


def main(tvdb_id: str, dir_path: Path):
    # auth and create var to access database
    tvdb = get_db.auth()

    # gets info from database, returns in dataclass
    info = get_db.show_info(tvdb, tvdb_id)

    # making extra info trees
    actor_tree = xml_t.actor(info.ext["characters"])
    art_tree = xml_t.artwork(info.ext["artworks"], info.ext["seasons"])

    # tvshow xml
    series_xml = xml_t.series(info, tvdb_id, actor_tree, art_tree)
    # writing show file
    series_out_path = dir_path / "tvshow.nfo"
    xml_t.output_xml(series_xml, series_out_path)

    # getting episode files
    episode_filelist = get_files(dir_path)
    # creating and writing episode loop
    xml_t.ep_xml_loop(info, episode_filelist, actor_tree)

    # asking if user wants to download art
    dt.art_download(info.ext["artworks"], dir_path, info.ext["seasons"])


if __name__ == "__main__":
    typer.run(main)
