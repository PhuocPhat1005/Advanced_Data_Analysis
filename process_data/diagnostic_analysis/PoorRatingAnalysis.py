import google.generativeai as genai
import pandas as pd
from scipy.stats import mannwhitneyu, kruskal, spearmanr, pearsonr
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression


class PoorRatingAnalysis(object):

    def __init__(self):
        pass

    @staticmethod
    def get_feature_types(df, factor_groups):
        import numpy as np
        if 'original_price' not in factor_groups:
            factor_groups = factor_groups + ['original_price']
        numeric_cols = df[factor_groups].select_dtypes(include=np.number).columns.tolist()
        category_cols = df[factor_groups].select_dtypes(exclude=np.number).columns.tolist()
        return numeric_cols, category_cols

    @staticmethod
    def split_rating_groups(df, rating_col):
        low_group = df[(df[rating_col] >= 1.0) & (df[rating_col] < 3.0)]
        high_group = df[df[rating_col] >= 3.0]
        return low_group, high_group

    @staticmethod
    def run_statistical_tests(df, rating_col, numeric_cols, category_cols):

        low_group, high_group = PoorRatingAnalysis.split_rating_groups(df, rating_col)
        results = {}

        for col in numeric_cols:
            stat_mw, p_mw = mannwhitneyu(low_group[col], high_group[col])
            corr_spearman, p_s = spearmanr(df[col], df[rating_col])
            corr_pearson, p_p = pearsonr(df[col], df[rating_col])
            results[col] = {
                'low_mean': float(low_group[col].mean()),
                'high_mean': float(high_group[col].mean()),
                'mean_diff': float(low_group[col].mean() - high_group[col].mean()),
                'mannwhitney_p': float(p_mw),
                'spearman_corr': float(corr_spearman),
                'spearman_p': float(p_s),
                'pearson_corr': float(corr_pearson),
                'pearson_p': float(p_p)
            }

        for col in category_cols:
            groups = [g[rating_col] for _, g in df.groupby(col)]
            stat_k, p_k = kruskal(*groups)
            avg_by_cat = df.groupby(col)[rating_col].mean().to_dict()
            results[col] = {
                'mean_by_category': {str(k): float(v) for k, v in avg_by_cat.items()},
                'kruskal_p': float(p_k)
            }

        return results

    @staticmethod
    def run_feature_importance(df, rating_col, numeric_cols, category_cols):
        X = pd.get_dummies(df[numeric_cols + category_cols], columns=category_cols)
        X = X.fillna(0)
        y = df[rating_col]
        print("Run fts importance")
        lr = LinearRegression()
        lr.fit(X, y)
        lr_importance = dict(zip(X.columns, map(float, lr.coef_)))
        print("\tDone lr importance")
        rf = RandomForestRegressor(random_state=42)
        rf.fit(X, y)
        rf_importance = dict(zip(X.columns, map(float, rf.feature_importances_)))
        print("\tDone rf importance")
        # perm = permutation_importance(rf, X, y, n_repeats=10, random_state=42)
        # perm_importance = dict(zip(X.columns, map(float, perm.importances_mean)))

        return {
            'linear_regression': lr_importance,
            'random_forest': rf_importance,
            # 'permutation_importance': perm_importance
        }

    @staticmethod
    def generate_explanations(stat_results, importance_results):
        root_causes = []
        recommendations = []

        for col, stats in stat_results.items():
            if 'mean_diff' in stats and stats['mannwhitney_p'] < 0.05:
                direction = 'higher' if stats['mean_diff'] > 0 else 'lower'
                root_causes.append(
                    f"{col} is {direction} in low-rating group (Δ={stats['mean_diff']:.2f}, p={stats['mannwhitney_p']:.3f})"
                )
                if direction == 'higher':
                    recommendations.append(f"Reduce {col} to improve rating")
                else:
                    recommendations.append(f"Increase {col} to improve rating")

            elif 'kruskal_p' in stats and stats['kruskal_p'] < 0.05:
                worst_cat = sorted(stats['mean_by_category'].items(), key=lambda x: x[1])[0]
                root_causes.append(
                    f"{col}={worst_cat[0]} has lowest average rating ({worst_cat[1]:.2f}, p={stats['kruskal_p']:.3f})"
                )
                recommendations.append(f"Review or avoid {col}={worst_cat[0]} for better rating")

        rf = importance_results['random_forest']
        if rf:
            top_rf = max(rf.items(), key=lambda x: x[1])
            root_causes.append(f"Top RF importance: {top_rf[0]} ({top_rf[1]:.3f})")

        return root_causes, recommendations

    @staticmethod
    def analyze(
        df,
        rating_col='rating_average',
        factor_groups=None,
        date_column=None,
        min_date=None,
        max_date=None
    ):
        df = df.copy()
        df = df[df[rating_col] >= 1]

        df[date_column] = pd.to_datetime(df[date_column])
        if min_date:
            df = df[df[date_column] >= pd.to_datetime(min_date)]
        if max_date:
            df = df[df[date_column] <= pd.to_datetime(max_date)]
        print(f"Filtered by date: {min_date} to {max_date} -> {len(df)} rows")

        numeric_cols, category_cols = PoorRatingAnalysis.get_feature_types(df, factor_groups)

        stats = PoorRatingAnalysis.run_statistical_tests(df, rating_col, numeric_cols, category_cols)
        print("Done statistical tests")

        importance = PoorRatingAnalysis.run_feature_importance(df, rating_col, numeric_cols, category_cols)
        print("Done feature importance")

        root_causes, recommendations = PoorRatingAnalysis.generate_explanations(stats, importance)
        print("Done explanation generation")

        return {
            'statistical_tests': stats,
            'feature_importance': importance,
            'root_causes': root_causes,
            'recommendations': recommendations
        }

    @staticmethod
    def analyze_reason(reason_json, api_key: str):
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        question = f"Dưới đây là một dictionary chứa thông tin phân tích nguyên nhân một sản phẩm đánh giá trung bình tệ (điểm từ 1 đến dưới 3) từ nhiều đầu phân tích và học máy khác nhau. Hãy tóm tắt và trình bày ngắn gọn các nguyên nhân rút được từ thông tin này:\nNội dung như sau: \n{str(reason_json)}";
        answer = model.generate_content(question)
        return answer.text.strip()
