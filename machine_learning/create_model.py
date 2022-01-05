import pandas as pd
import numpy as np
import pickle
import os
import warnings
from datetime import datetime
from sklearn.linear_model import LogisticRegression


warnings.simplefilter('ignore', UserWarning)


def date_diff(date):
    date = date[:11]
    date_in_datetime = datetime.strptime(date, " %Y-%m-%d")
    today_in_datetime = datetime.now()
    day_diff_in_datetime = (today_in_datetime - date_in_datetime).days
    return int(day_diff_in_datetime)


def create_model(df, file_name="latest"):
    """
    入力したデータを全て学習に使用して、モデルを作成する。

    Args:
        df (pandas.DataFrame): rawデータ
        file_name (str): 保存するときのファイル名。保存はmachine_learning/modelの中に入る

    Return:
        None
    """
    
    # preprocess raw data
    df["length_caption"] = df["caption"].map(lambda x: len(x))
    df["tag"] = df["caption"].map(lambda x: x.count('#'))
    df["mention"] = df["caption"].map(lambda x: x.count("@"))
    df["date_diff"] = df["date"].map(date_diff)
    df["like_ratio_follower"] = df["good"] / df["follower"]
    df["like_ratio_date_diff"] = df["good"] / df["date_diff"]

    df = df[["label", "length_caption", "tag", "mention", "like_ratio_follower", "like_ratio_date_diff", "follower", "following"]]

    # prepare data for test
    X_all = df.drop(columns=["label"])
    y_all = df["label"]

    # train model
    model = LogisticRegression(random_state=42)
    model.fit(X_all, y_all)
    
    pickle.dump(model, open(os.path.join('machine_learning/model',file_name), 'wb'))
    
    return None


if __name__ == '__main__':
    df = pd.read_csv('machine_learning/template.csv')
    file_name = "1"
    
    create_model(df, file_name)
    
    loaded_model = pickle.load(open(os.path.join('machine_learning/model',file_name), 'rb'))
    
    result = loaded_model.predict([[10, 0, 0, 0.1, 0.01, 100, 100]])
    print(result)

