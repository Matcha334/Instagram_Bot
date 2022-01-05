import pandas as pd
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


def date_diff(date):
    date = date[:11]
    date_in_datetime = datetime.strptime(date, " %Y-%m-%d")
    today_in_datetime = datetime.now()
    day_diff_in_datetime = (today_in_datetime - date_in_datetime).days
    return int(day_diff_in_datetime)


def learning(df):
    """
    入力したデータを学習データ、評価データを 0.75 : 0.25 で分ける。
    学習データを用いてモデルを学習し、残りの評価データを用いてモデルを評価する。

    Args:
        df (pandas.DataFrame): rawデータ

    Return:
        float: 0-1で評価する。
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
    X_train, X_test, y_train, y_test = train_test_split(X_all, y_all, random_state=42)

    # train model
    model = LogisticRegression(random_state=42)
    model.fit(X_train, y_train)

    # predict model
    y_prediction = model.predict(X_test)

    # evaluate
    score = accuracy_score(y_test, y_prediction)
    
    return score


if __name__ == '__main__':
    df = pd.read_csv('machine_learning/template.csv')
    
    score = learning(df)
    
    print(score)

