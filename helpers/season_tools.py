# returns the amount of alternate seasons
def season_amount(s_list):
    return sum(seasons["type"]["type"] == "alternate" for seasons in s_list)


# returns the season number of a season ID
def season_num(s_list, s_id):
    return next(season["number"] for season in s_list if season["id"] == s_id)
