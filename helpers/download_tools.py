# BUILT IN IMPORTS
import urllib.request
from dataclasses import dataclass

# LOCAL IMPORTS
import helpers.season_tools as st


@dataclass
class filecounts:
    banner: int = 0
    poster: int = 0
    fanart: int = 0
    clrArt: int = 0
    clrLogo: int = 0
    unknown: int = 0


# downloads art for show
def art_download(art_inf, series_path, s_list):
    cnt = filecounts()
    season_cnt = {}

    for art in art_inf:
        match art["type"]:
            case 1:  # banner
                filename = series_path / ("banner" + str(cnt.banner).zfill(2) + ".jpg")
                cnt.banner += 1
            case 2:  # poster
                filename = series_path / ("poster" + str(cnt.poster).zfill(2) + ".jpg")
                cnt.poster += 1
            case 3:  # fanart/background
                filename = series_path / ("fanart" + str(cnt.fanart).zfill(2) + ".jpg")
                cnt.fanart += 1
            case 7:  # season
                sn = st.season_num(s_list, art["seasonId"])
                if not season_cnt.get(sn):
                    season_cnt[sn] = 0
                filename = series_path / (
                    "season"
                    + str(sn).zfill(2)
                    + "-poster"
                    + str(season_cnt[sn]).zfill(2)
                    + ".jpg"
                )
                season_cnt[sn] += 1
            case 22:  # clearart
                filename = series_path / (
                    "clearart" + str(cnt.clrArt).zfill(2) + ".jpg"
                )
                cnt.clrArt += 1
            case 23:  # clearlogo
                filename = series_path / (
                    "clearlogo" + str(cnt.clrLogo).zfill(2) + ".jpg"
                )
                cnt.clrLogo += 1
            case _:  # unknown
                filename = series_path / (
                    "UNKNOWN" + str(cnt.unknown).zfill(2) + ".jpg"
                )
                cnt.unknown += 1

        print("Downloading " + filename.name)
        urllib.request.urlretrieve(art["image"], filename)
