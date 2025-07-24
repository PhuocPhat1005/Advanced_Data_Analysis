import pandas as pd
import os

from common import ROOT_PATH

DATA_DIR = os.path.join(ROOT_PATH, "data")

product_revenue_df       = pd.read_csv(os.path.join(DATA_DIR, "Products_Revenue.csv"))
product_display_status_df = pd.read_csv(os.path.join(DATA_DIR, "Products_DisplayStatus.csv"))
product_quantity_df      = pd.read_csv(os.path.join(DATA_DIR, "Products_Quantity.csv"))
product_rating_df        = pd.read_csv(os.path.join(DATA_DIR, "Products_Rating.csv"))
rating_root_cause_df     = pd.read_csv(os.path.join(DATA_DIR, "Rating_RootCause.csv"))
status_root_cause_df     = pd.read_csv(os.path.join(DATA_DIR, "Status_RootCause.csv"))
