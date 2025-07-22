import pandas as pd


class DisplayStatusAnalysis(object):

    def __init__(self):
        return

    @staticmethod
    def getDisplayStatusByFactor(df, status_column="", factor_column="", date_column="", min_date="2016-01-01", max_date=""):
        df = df.copy()

        df[date_column] = pd.to_datetime(df[date_column])
        df = df[
            (df[date_column] >= pd.to_datetime(min_date)) &
            (df[date_column] <= pd.to_datetime(max_date))
        ]

        result = (
            df.groupby([factor_column, status_column])
            .size()
            .reset_index(name="count")
        )

        return result.to_dict(orient='records')
