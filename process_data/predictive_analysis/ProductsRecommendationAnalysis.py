class ProductsRecommendationAnalysis(object):
    def __init__(self):
        pass

    @staticmethod
    def recommend(df, name_column="", sim_column="sim", name_product="", topk=5):
        results = df[df[name_column] == name_product].sort_values(sim_column, ascending=False).head(topk)
        results = results[["name_dst", "brand_dst", "category_dst"]]
        return results.to_dict(orient='records')
    @staticmethod
    def list_product_names(df, name_column="name"):
        if name_column not in df.columns:
            raise ValueError(f"Column '{name_column}' not found in DataFrame.")
        
        names = df[name_column].dropna().tolist()
        unique_names = list(dict.fromkeys(names))  # preserve order & remove duplicates
        return unique_names
