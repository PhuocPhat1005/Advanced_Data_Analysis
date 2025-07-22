class RatingAnalysis(object):

    def __init__():
        return

    @staticmethod
    def getReviewCountByFactor(df, review_count_column="", factor_column="", by_function="sum"):
        import pandas as pd

        df = df.copy()

        df = df[df[review_count_column] > 0]

        if by_function == "sum":
            result = (
                df.groupby(factor_column)[review_count_column]
                .sum()
                .reset_index()
                .rename(columns={review_count_column: "review_count_sum"})
            )
        elif by_function == "mean":
            result = (
                df.groupby(factor_column)[review_count_column]
                .mean()
                .reset_index()
                .rename(columns={review_count_column: "review_count_mean"})
            )
        else:
            raise ValueError("by_function must be either 'sum' or 'mean'")

        return result.to_json(orient='records', force_ascii=False)

    @staticmethod
    def getAvgRatingByFactors(df, rating_column="", factor_columns=""):
        import pandas as pd

        df = df.copy()
        df = df[df[rating_column]>0]

        if isinstance(factor_columns, str):
            factor_columns = [factor_columns]

        result = (
            df.groupby(factor_columns)[rating_column]
            .mean()
            .reset_index()
            .rename(columns={rating_column: "avg_rating"})
        )

        return result.to_json(orient='records', force_ascii=False)