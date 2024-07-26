# BUILT IN IMPORTS
import xml.etree.ElementTree as ET
from datetime import datetime
from operator import itemgetter

# LOCAL IMPORTS
import helpers.season_tools as st


# outputs xml data
def output_xml(el_tree, out_path):
    output = ET.ElementTree(el_tree)
    with open(out_path, "wb") as file:
        output.write(file, "UTF-8", True)


# returns an xml tree with show's artwork
def artwork(art_inf, sea_inf):
    art_tree_temp = ET.Element("temp")
    fa_tree_temp = ET.Element("fanart")
    for art in art_inf:
        art_link = art["image"]
        match art["type"]:
            case 1:  # banner
                art_se = ET.SubElement(art_tree_temp, "thumb")
                art_se.set("aspect", "banner")
            case 2:  # poster
                art_se = ET.SubElement(art_tree_temp, "thumb")
                art_se.set("aspect", "poster")
            case 3:  # fanart/background
                art_se = ET.SubElement(fa_tree_temp, "thumb")
            case 7:  # season
                art_se = ET.SubElement(art_tree_temp, "thumb")
                s_num = str(st.season_num(sea_inf, art["seasonId"]))
                art_se.set("aspect", "poster")
                art_se.set("type", "season")
                art_se.set("season", s_num)
            case 22:  # clearart
                art_se = ET.SubElement(art_tree_temp, "thumb")
                art_se.set("aspect", "clearart")
            case 23:  # clearlogo
                art_se = ET.SubElement(art_tree_temp, "thumb")
                art_se.set("aspect", "clearlogo")
            case _:  # unknown
                art_se = ET.SubElement(art_tree_temp, "thumb")
        art_se.set("preview", art_link)
        art_se.text = art_link
    art_tree_temp.append(fa_tree_temp)
    return art_tree_temp


# returns an xml tree with show's actors
def actor(act_inf):
    act_inf_s = sorted(act_inf, key=itemgetter("sort"))
    act_temp = ET.Element("temp")
    for actor in act_inf_s:
        order_num = str(actor["sort"])
        act_subtree = ET.SubElement(act_temp, "actor")
        ET.SubElement(act_subtree, "name").text = actor["personName"]
        ET.SubElement(act_subtree, "role").text = actor["name"]
        ET.SubElement(act_subtree, "order").text = order_num
        ET.SubElement(act_subtree, "thumb").text = actor["personImgURL"]
    return act_temp


# returns an xml of the tv show's metadata
def series(inf, show_id, actor_tree, art_tree):
    # var setting
    fa_link = inf.ext["artworks"][1]["image"]
    ep_len = str(len(inf.eps["episodes"]))
    sea_len = str(st.season_amount(inf.ext["seasons"]))
    date_time = str(datetime.now())

    # show tree
    show_xml = ET.Element("tvshow")
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
    show_xml.extend(art_tree)
    # fanart doesnt work; TODO download artworks?
    fa = ET.SubElement(show_xml, "fanart")
    fa_thumb = ET.SubElement(fa, "thumb")
    fa_thumb.set("preview", fa_link)
    fa_thumb.text = fa_link
    show_xml.extend(actor_tree)
    gen = ET.SubElement(show_xml, "generator")
    ET.SubElement(gen, "appname").text = "QuickMediaScraper.py"
    ET.SubElement(gen, "kodiversion").text = "20"
    ET.SubElement(gen, "datetime").text = date_time
    ET.indent(show_xml, "    ")
    return show_xml


# returns an xml of an episode's metadata
def episode(inf, ep_inf, s_title, mpaa, studio, actor_tree):
    # var setting
    ep_id = str(ep_inf["id"])
    ep_season = str(ep_inf["seasonNumber"])
    ep_num = str(ep_inf["number"])
    date_time = str(datetime.now())

    print(
        "Working on S"
        + ep_season.zfill(2)
        + "E"
        + ep_num.zfill(2)
        + " - "
        + ep_inf["name"]
    )

    # episode tree
    ep_xml = ET.Element("episodedetails")
    ET.SubElement(ep_xml, "title").text = ep_inf["name"]
    ET.SubElement(ep_xml, "showtitle").text = s_title
    uid = ET.SubElement(ep_xml, "uniqueid")
    uid.set("default", "true")
    uid.set("type", "tvdb")
    uid.text = ep_id
    ET.SubElement(ep_xml, "ratings")
    ET.SubElement(ep_xml, "userrating").text = "0"
    ET.SubElement(ep_xml, "top250").text = "0"
    ET.SubElement(ep_xml, "season").text = ep_season
    ET.SubElement(ep_xml, "episode").text = ep_num
    ET.SubElement(ep_xml, "plot").text = ep_inf["overview"]
    ET.SubElement(ep_xml, "mpaa").text = mpaa
    ET.SubElement(ep_xml, "playcount").text = "0"
    ET.SubElement(ep_xml, "lastplayed")
    ET.SubElement(ep_xml, "aired").text = ep_inf["aired"]
    ET.SubElement(ep_xml, "studio").text = studio
    ET.SubElement(ep_xml, "credits")
    ET.SubElement(ep_xml, "director")
    ET.SubElement(ep_xml, "thumb").text = ep_inf["image"]
    ep_xml.extend(actor_tree)
    ET.SubElement(ep_xml, "fileinfo")
    gen = ET.SubElement(ep_xml, "generator")
    ET.SubElement(gen, "appname").text = "quickMediaScrape.py"
    ET.SubElement(gen, "kodiversion").text = "20"
    ET.SubElement(gen, "datetime").text = date_time
    ET.indent(ep_xml, "    ")
    return ep_xml


# loops through episodes, creates trees and writes them
def ep_xml_loop(inf, ep_filelist, act_tree):
    # these vars are the same every ep, so define them here
    show_title = inf.tra["name"]
    mpaa_rating = inf.ext["contentRatings"][0]["name"]
    studio = inf.ext["companies"][0]["name"]
    for cnt, eps in enumerate(ep_filelist):
        ep_inf = inf.eps["episodes"][cnt]
        ep_out_path = eps.with_suffix(".nfo")
        ep_xml = episode(inf, ep_inf, show_title, mpaa_rating, studio, act_tree)
        output_xml(ep_xml, ep_out_path)
