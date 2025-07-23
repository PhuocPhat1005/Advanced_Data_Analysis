import pandas as pd
import numpy as np
import os
import sys
import json
import re

import warnings

from diagnostic_analysis import PoorRatingAnalysis
warnings.filterwarnings("ignore")

import matplotlib.pyplot as plt
import seaborn as sns

from descriptive_analysis.RevenueStatusAnalysis import RevenueStatusAnalysis
from descriptive_analysis.RatingAnalysis import RatingAnalysis
from descriptive_analysis.QuantityAnalysis import QuantityAnalysis
from descriptive_analysis.DisplayStatusAnalysis import DisplayStatusAnalysis

from diagnostic_analysis.StatusDiagnosticAnalysis import StatusDiagnosticAnalysis
from diagnostic_analysis.PoorRatingAnalysis import PoorRatingAnalysis



#t = RevenueStatusAnalysis.getRevenueByTimeline(df, revenue_column="revenue", categorized_column="category", timeline_column="date_created", time_mode="M")
#t = RevenueStatusAnalysis.getTotalRevenue(df, revenue_column="revenue", categorized_column="current_seller", date_column="date_created", max_date="2020-01-03")
#print(t[t.category == "Thời Trang"].head(30))

#t = StatusDiagnosticAnalysis.diagnostic_analysis(df, target_col="status", factor_groups=["category", "product_source", "original_price", "name_length"])
#t = RatingAnalysis.getAvgRatingByFactors(df, rating_column="rating_average", factor_columns="category")
#t = RatingAnalysis.getReviewCountByFactor(df, review_count_column="review_count", factor_column="current_seller", by_function="sum")
#t = QuantityAnalysis.getQuantityOfProductsByFactorGroup(\
#    df,\
#    quantity_column="quantity_sold",\
#    factor_group_columns=["brand", "current_seller"],\
#    date_column="date_created",\
#    min_date="2022-01-01",\
#    max_date="2023-06-01"
#    )
#t = DisplayStatusAnalysis.getDisplayStatusByFactor(\
#    df,\
#    status_column="status",\
#    factor_column="category",\
#    date_column="date_created",\
#    min_date="2022-01-01",\
#    max_date="2023-06-01"
#    )

#
#print(t)
#with open("./data/diagnostic_analysis.json", "w", encoding="utf-8") as f:
#    json.dump(t, f, ensure_ascii=False, indent=2)

"""
REVENUE"""
#df = pd.read_csv("D:/career/master/data_analysis/ck/Advanced_Data_Analyst/data/Products_Revenue.csv")

#t = RevenueStatusAnalysis.getRevenueByTimeline(df, revenue_column="revenue", categorized_column="category", timeline_column="date_created", time_mode="M")
#
#DF = pd.DataFrame(json.loads(t))
#DF["time_group"] = pd.to_datetime(DF["time_group"], unit='ms')
#print(DF.category.value_counts())

"""
Thời Trang                61
Phụ kiện vali             55
Phụ kiện thời trang nữ    54
"""
"""
list_categories = ["Phụ kiện vali", "Phụ kiện thời trang nữ"]

t = DF[DF.category.isin(list_categories)]


plt.figure(figsize=(10,4))
ax = sns.lineplot(t, x="time_group", y="total_revenue", hue="category")
plt.show()
"""
"""
t = RevenueStatusAnalysis.getTotalRevenue(df, revenue_column="revenue", categorized_column="current_seller", date_column="date_created", min_date="2019-10-09", max_date="2020-01-03")

DF = pd.DataFrame(json.loads(t))

print(DF.head(5))

#plt.figure(figsize=(6,4))

ax = sns.barplot(DF.head(10), y="current_seller", x="total_revenue")

plt.show()
"""

"""QUANTITY
"""
"""
df = pd.read_csv("D:/career/master/data_analysis/ck/Advanced_Data_Analyst/data/Products_Quantity.csv")

t = QuantityAnalysis.getQuantityOfProductsByFactorGroup(\
    df,\
    quantity_column="quantity_sold",\
    factor_group_columns=["brand", "current_seller"],\
    date_column="date_created",\
    min_date="2022-01-01",\
    max_date="2023-06-01"
    )

DF = pd.DataFrame(json.loads(t))

print(DF.head())

ax = sns.barplot(DF[(DF.brand == "\tOEM")&(DF.total_quantity > 100)].head(10), y="current_seller", x="total_quantity")

plt.show()
"""

"""
df = pd.read_csv("D:/career/master/data_analysis/ck/Advanced_Data_Analyst/data/Products_Rating.csv")

t = RatingAnalysis.getAvgRatingByFactors(df, rating_column="rating_average", factor_columns=["category"])

DF = pd.DataFrame(json.loads(t))

print(DF.head())

ax = sns.barplot(DF.head(10), y="category", x="avg_rating")

plt.show()"""

"""
df = pd.read_csv("D:/career/master/data_analysis/ck/Advanced_Data_Analyst/data/Products_Rating.csv")

t = RatingAnalysis.getReviewCountByFactor(df, review_count_column="review_count", factor_column="category", by_function="sum")

DF = pd.DataFrame(json.loads(t))

print(DF.head())

ax = sns.barplot(DF.head(10), y="category", x="review_count_sum")

plt.show()"""

"""
df = pd.read_csv("D:/career/master/data_analysis/ck/Advanced_Data_Analyst/data/Products_DisplayStatus.csv")

t = DisplayStatusAnalysis.getDisplayStatusByFactor(\
df, \
status_column="status", \
factor_column="category", \
date_column="date_created", \
min_date="2023-01-01", \
max_date="2024-01-01"\
)

DF = pd.DataFrame(json.loads(t))

print(DF.head())

ax = sns.barplot(DF.head(10), y="category", x="count", hue="status")

plt.show()
"""

"""
df = pd.read_csv("D:/career/master/data_analysis/ck/Advanced_Data_Analyst/data/Status_RootCause.csv")
t = StatusDiagnosticAnalysis.diagnostic_analysis(df,\
                                                 target_col="status",\
                                                 factor_groups=["brand", "category", "brand", "has_video", "number_of_images", "name_length", "original_price"],\
                                                 date_column="date_created",\
                                                 min_date="2023-01-01",\
                                                 max_date="2023-07-01"
                                                 )
#with open("./data/diagnostic_analysis.json", "w", encoding="utf-8") as f:
#    json.dump(t, f, ensure_ascii=False, indent=2)
content = StatusDiagnosticAnalysis.analyze_reason(t)

print(content)
"""

df = pd.read_csv("D:/career/master/data_analysis/ck/Advanced_Data_Analyst/data/Rating_RootCause.csv")
t = PoorRatingAnalysis.analyze(df,\
                               rating_col="rating_average",\
                               factor_groups=["brand", "category", "current_seller", "has_video", "number_of_images", "name_length", "original_price"],\
                               date_column="date_created",\
                               min_date="2023-01-01",\
                               max_date="2023-07-01"
                               )
#with open("./data/diagnostic_analysis.json", "w", encoding="utf-8") as f:
#    json.dump(t, f, ensure_ascii=False, indent=2)
content = PoorRatingAnalysis.analyze_reason(t)

print(content)
