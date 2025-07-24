class ProductsRecommendationAnalysis(object):
    def __init__(self):
        pass

    @staticmethod
    def recommend(df, name_column="", sim_column="sim", name_product="", topk=5):
        results = df[df[name_column] == name_product].sort_values(sim_column, ascending=False).head(topk)
        results = results[["name_dst", "brand_dst", "category_dst"]]
        return results.to_dict(orient='records')
