class QuantityAnalysis(object):

    def __init__():
	
        return

    @staticmethod
    def getQuantityOfProductsByFactorGroup(df, quantity_column="", factor_group_columns="", date_column="", min_date="2016-01-01", max_date=""):
        import pandas as pd
 
        df = df.copy()
 
        if isinstance(factor_group_columns, str):
            factor_group_columns = [factor_group_columns]
 
        df[date_column] = pd.to_datetime(df[date_column])
        df = df[
            (df[date_column] >= pd.to_datetime(min_date)) &
            (df[date_column] <= pd.to_datetime(max_date))
        ]
 
        result = (
            df.groupby(factor_group_columns)[quantity_column]
            .sum()
            .reset_index()
            .rename(columns={quantity_column: "total_quantity"})
        )
 
        return result.to_json(orient='records', force_ascii=False)