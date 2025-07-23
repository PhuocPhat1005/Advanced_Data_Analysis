import pandas as pd

from common import ROOT_PATH

product_revenue_df = pd.read_csv(ROOT_PATH + "\data\Products_Revenue.csv")
product_display_status_df = pd.read_csv(ROOT_PATH + "\data\Products_DisplayStatus.csv")
product_quantity_df = pd.read_csv(ROOT_PATH + "\data\Products_Quantity.csv")
product_rating_df = pd.read_csv(ROOT_PATH + "\data\Products_Rating.csv")
