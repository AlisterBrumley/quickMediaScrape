# BUILT IN IMPORTS
from pathlib import Path

# DEPENDENCY IMPORTS
import typer

# LOCAL IMPORTS
import helpers.xml_tools as xml_t
import helpers.database_tools as get_db
import helpers.download_tools as dt


def main(tvdb_id: str, dir_path: Path):
    # auth and create var to access database
    print("Authorizing...")
    tvdb = get_db.auth()

    # gets info from database, returns in dataclass
    print("Getting info from database...")
    info = get_db.show_info(tvdb, tvdb_id)

    # making extra info trees
    print("Making xml tree for actors")
    actor_tree = xml_t.actor(info.ext["characters"])
    print("Making xml tree for artworks")
    art_tree = xml_t.artwork(info.ext["artworks"], info.ext["seasons"])

    # tvshow xml
    print("Making tvshow xml")
    series_xml = xml_t.series(info, tvdb_id, actor_tree, art_tree)
    series_out_path = dir_path / "tvshow.nfo"
    xml_t.output_xml(series_xml, series_out_path)

    # episode xml's
    print("Making episode xml's")
    episode_filelist = sorted(dir_path.rglob("*.mkv"))
    xml_t.ep_xml_loop(info, episode_filelist, actor_tree)

    # download art
    answer = input("Do you want to download artwork(y/N)? ").lower().strip()
    if answer == "y":
        dt.art_download(info.ext["artworks"], dir_path, info.ext["seasons"])
    print("Completed!")


if __name__ == "__main__":
    typer.run(main)
