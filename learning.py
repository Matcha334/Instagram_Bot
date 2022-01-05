import pandas as pd
from datetime import datetime


def date_diff(date):
    date = date[:11]
    date_in_datetime = datetime.strptime(date, " %Y-%m-%d")
    today_in_datetime = datetime.now()
    day_diff_in_datetime = (today_in_datetime - date_in_datetime).days
    return int(day_diff_in_datetime)


df = pd.read_csv('template.csv')
df["length_caption"] = df["caption"].map(lambda x: len(x))
df["tag"] = df["caption"].map(lambda x: x.count('#'))
df["mention"] = df["caption"].map(lambda x: x.count("@"))
df["like_ratio_follower"] = df["good"] / df["follower"]
df["like_ratio_date_diff"] = df["good"] / df["date_diff"]

df = df[["label", "length_caption", "tag", "mention", "like_ratio_follower", "like_ratio_date_diff", "follower", "following"]]