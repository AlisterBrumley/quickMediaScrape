# Quick Media Scraper
Scrapes TVBD for alternate seasons and outputs in kodi `.nfo` files. Useful for anime dubs, or alternate show orders.

### Usage
This program requires a TVDB ID, and a directory for the location of the show<br>
eg. `python3 quickMediaScrape.py ${SHOW_ID} ${SHOW_DIR}` <br>
eg. `python3 quickMediaScrape.py 78500 "~/TV/Sailor Moon"` <br>
It will then authorize with TVDB, download metadata and create `.nfo` files for the show and episodes.

### Artwork
Once it's finished creating `.nfo` files, it asks if you want to download artwork. It will download all artworks attached to the the show **This will take a while!** 

#### Where does it put things?
```
/TV_SHOW
    |____/S1
    |   |___SHOW_S01E01.MP4
    |   |___SHOW_S01E01.NFO
    |   |___SHOW_S01E02.MP4
    |   |___SHOW_S01E02.NFO
    |___tv_show.nfo
    |___poster00.jpg
    |___poster01.jpg
    |___banner00.jpg
```

### Licensing and Attribution
<div>
<a class="thetvdbattribution" style="" href="https://thetvdb.com/subscribe">
    <img src="https://thetvdb.com/images/attribution/logo1.png" height="45" style="vertical-align:middle">
    <span>Metadata provided by TheTVDB. Please consider adding missing information or subscribing.</span>
</a>
</div>