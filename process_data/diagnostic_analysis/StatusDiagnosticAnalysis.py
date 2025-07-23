class StatusDiagnosticAnalysis(object):

    def __init__(self):
        pass

    @staticmethod
    def get_feature_types(df, target_col, factor_groups=None):
        import numpy as np

        if factor_groups is None:
            factor_groups = df.columns.drop(target_col).tolist()

        numeric_cols = df[factor_groups].select_dtypes(include=np.number).columns.tolist()
        category_cols = df[factor_groups].select_dtypes(exclude=np.number).columns.tolist()
        return numeric_cols, category_cols

    @staticmethod
    def calculate_distribution(df, target_col, numeric_cols, category_cols):
        import pandas as pd

        dist = {}
        for col in numeric_cols:
            dist[col] = {
                'status_0': {
                    'mean': float(df[df[target_col] == 0][col].mean()),
                    'median': float(df[df[target_col] == 0][col].median())
                },
                'status_1': {
                    'mean': float(df[df[target_col] == 1][col].mean()),
                    'median': float(df[df[target_col] == 1][col].median())
                }
            }

        for col in category_cols:
            try:
                cross_tab = pd.crosstab(df[col], df[target_col], normalize='index') * 100
                dist[col] = {
                    'percentage_status_1': {str(k): float(v) for k, v in cross_tab.get(1, pd.Series()).to_dict().items()}
                }
            except Exception:
                dist[col] = {'percentage_status_1': {}}
        return dist

    @staticmethod
    def run_hypothesis_tests(df, target_col, numeric_cols, category_cols):
        import pandas as pd
        from scipy.stats import ttest_ind, mannwhitneyu, chi2_contingency

        tests = {}
        for col in numeric_cols:
            group0 = df[df[target_col] == 0][col].dropna()
            group1 = df[df[target_col] == 1][col].dropna()
            try:
                if len(group0) > 30 and len(group1) > 30:
                    stat, p = ttest_ind(group0, group1, equal_var=False)
                else:
                    stat, p = mannwhitneyu(group0, group1)
                tests[col] = {
                    'p_value': float(p),
                    'significant': str(p < 0.05)
                }
            except Exception:
                tests[col] = {'p_value': None, 'significant': False}

        for col in category_cols:
            try:
                contingency = pd.crosstab(df[col], df[target_col])
                chi2, p, _, _ = chi2_contingency(contingency)
                tests[col] = {
                    'p_value': float(p),
                    'significant': str(p < 0.05)
                }
            except Exception:
                tests[col] = {'p_value': None, 'significant': str(False)}

        return tests

    @staticmethod
    def analyze_feature_importance(df, target_col, numeric_cols, category_cols):
        import pandas as pd
        import numpy as np
        from sklearn.linear_model import LogisticRegression
        from sklearn.ensemble import RandomForestClassifier

        try:
            X = pd.get_dummies(df[numeric_cols + category_cols], columns=category_cols)
            X = X.fillna(0)
            y = df[target_col]

            lr = LogisticRegression(max_iter=1000)
            lr.fit(X, y)
            odds_ratio = np.exp(lr.coef_[0])
            lr_importance = dict(zip(X.columns, map(float, odds_ratio)))

            rf = RandomForestClassifier()
            rf.fit(X, y)
            rf_importance = dict(zip(X.columns, map(float, rf.feature_importances_)))

            return {
                'logistic_regression_odds_ratio': lr_importance,
                'random_forest_importance': rf_importance
            }
        except Exception:
            return {
                'logistic_regression_odds_ratio': {},
                'random_forest_importance': {}
            }

    @staticmethod
    def identify_root_causes(distribution, hypothesis_tests, feature_importance):
        root_causes = []
        recommendations = []

        for col, test in hypothesis_tests.items():
            if test.get('significant') == "True":
                dist = distribution.get(col, {})
                if 'status_0' in dist and 'mean' in dist['status_0']:
                    mean_diff = dist['status_1']['mean'] - dist['status_0']['mean']
                    direction = "higher" if mean_diff > 0 else "lower"
                    root_causes.append(
                        f"{col} is {direction} for status=1 (p={test['p_value']:.3f})"
                    )
                elif 'percentage_status_1' in dist:
                    for cat, percent in dist['percentage_status_1'].items():
                        if percent > 50:
                            root_causes.append(
                                f"{col}={cat} has {percent:.1f}% status=1 (p={test['p_value']:.3f})"
                            )

        rf_importance = feature_importance.get('random_forest_importance', {})
        if rf_importance:
            top_feature = max(rf_importance.items(), key=lambda x: x[1])
            root_causes.append(
                f"Most important feature (Random Forest): {top_feature[0]} (importance={top_feature[1]:.3f})"
            )

        for cause in root_causes:
            if "is higher" in cause:
                var = cause.split()[0]
                recommendations.append(f"Reduce {var} to lower status=1 risk")
            elif "is lower" in cause:
                var = cause.split()[0]
                recommendations.append(f"Increase {var} to lower status=1 risk")
            elif "=" in cause and "%" in cause:
                var, val = cause.split("=")[0], cause.split("=")[1].split()[0]
                recommendations.append(f"Avoid {var}={val} to reduce status=1")

        return root_causes, recommendations

    @staticmethod
    def diagnostic_analysis( 
        df, 
        target_col='status', 
        factor_groups=None,
        date_column=None,
        min_date=None,
        max_date=None
    ):
        print("Start diagnostic analysis")

        import pandas as pd

        df[date_column] = pd.to_datetime(df[date_column], errors='coerce')
        if min_date:
            df = df[df[date_column] >= pd.to_datetime(min_date)]
        if max_date:
            df = df[df[date_column] <= pd.to_datetime(max_date)]
        print(f"Filtered by date: {min_date} to {max_date} -> {len(df)} rows")

        numeric_cols, category_cols = StatusDiagnosticAnalysis.get_feature_types(df, target_col, factor_groups)

        distribution = StatusDiagnosticAnalysis.calculate_distribution(df, target_col, numeric_cols, category_cols)
        print("Done data distribution")

        hypothesis_tests = StatusDiagnosticAnalysis.run_hypothesis_tests(df, target_col, numeric_cols, category_cols)
        print("Done hypothesis tests")

        feature_importance = StatusDiagnosticAnalysis.analyze_feature_importance(df, target_col, numeric_cols, category_cols)
        print("Done feature importance")

        root_causes, recommendations = StatusDiagnosticAnalysis.identify_root_causes(distribution, hypothesis_tests, feature_importance)
        print("Done root cause analysis")

        return {
            'data_distribution': distribution,
            'hypothesis_tests': hypothesis_tests,
            'feature_importance': feature_importance,
            'root_causes': root_causes,
            'recommendations': recommendations
        }

    @staticmethod 
    def analyze_reason(reason_json):
        import google.generativeai as genai
        genai.configure(api_key="...")
        model = genai.GenerativeModel("gemini-1.5-flash")
        question = f"Dưới đây là một dictionary chứa thông tin phân tích nguyên nhân trưng bày chết (status=1) từ nhiều đầu phân tích và học máy khác nhau. Hãy tóm tắt và trình bày ngắn gọn các nguyên nhân rút được từ thông tin này:\nNội dung như sau: \n{str(reason_json)}";
        answer = model.generate_content(question)
        return answer.text.strip()
