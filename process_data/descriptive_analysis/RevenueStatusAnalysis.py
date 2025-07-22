class RevenueStatusAnalysis(object):

    def __init__():

        return;

    @staticmethod
    def getRevenueByTimeline(df, revenue_column="", categorized_column="", timeline_column="", time_mode="D"):
        import pandas as pd
        df = df.copy()
        df[timeline_column] = pd.to_datetime(df[timeline_column])
        if time_mode == "D":
            df["time_group"] = df[timeline_column].dt.date
        elif time_mode == "M":
            df["time_group"] = df[timeline_column].dt.to_period("M").dt.to_timestamp()
        elif time_mode == "Y":
            df["time_group"] = df[timeline_column].dt.to_period("Y").dt.to_timestamp()
        else:
            raise ValueError("time_mode must be 'D', 'M', or 'Y'")

        group_by_cols = ["time_group"]
        if categorized_column != "":
            group_by_cols.append(categorized_column)

        result = df.groupby(group_by_cols)[revenue_column].sum().reset_index()
        result = result.rename(columns={revenue_column: "total_revenue"})

        return result.to_json(orient='records', force_ascii=False)

    @staticmethod
    def getTotalRevenue(df, revenue_column="", categorized_column="", date_column="", min_date="2016-01-01", max_date=""):
        import pandas as pd

        df = df.copy()

        df[date_column] = pd.to_datetime(df[date_column])
        df = df[
            (df[date_column] >= pd.to_datetime(min_date)) &
            (df[date_column] <= pd.to_datetime(max_date))
        ]

        if categorized_column != "":
            result = (
                df.groupby(categorized_column)[revenue_column]
                .sum()
                .reset_index()
                .rename(columns={revenue_column: "total_revenue"})
            )
        else:
            total = df[revenue_column].sum()
            result = pd.DataFrame([{"total_revenue": total}])

        return result.to_json(orient='records', force_ascii=False)



