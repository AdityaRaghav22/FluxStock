import random as r
from datetime import datetime
from database.db_raw import get_raw_skus
from database.db_semi import get_semi_skus
from database.db_finished import get_finished_skus

def add_raw_sku(product_name, category):
  prefix = category[:3].upper()
  base = product_name[:3].upper()
  existing_skus = get_raw_skus()
  for _ in range(100):
    sku = f"{prefix}-{base}{r.randint(100, 999)}"
    if sku not in existing_skus:
      return sku
  raise Exception("[X] Failed to generate unique SKU after 100 attempts.") 
  
def add_semi_sku(product_name, category):
  prefix = category[:3].upper()
  base = product_name[:3].upper()
  existing_skus = get_semi_skus()
  for _ in range(100):
    sku = f"{prefix}-{base}{r.randint(100, 999)}"
    if sku not in existing_skus:
      return sku
  raise Exception("[X] Failed to generate unique SKU after 100 attempts.") 
  
def add_finished_sku(product_name, category):
  prefix = category[:3].upper()
  base = product_name[:3].upper()
  existing_skus = get_finished_skus()
  for _ in range(100):
    sku = f"{prefix}-{base}{r.randint(100, 999)}"
    if sku not in existing_skus:
      return sku
  raise Exception("[X] Failed to generate unique SKU after 100 attempts.") 

def get_valid_date():
  while True:
    date_str = input("Enter Date (DD-MM-YYYY): ")
    try:
      sales_order_date = datetime.strptime(date_str, "%d-%m-%Y").date()
      return str(sales_order_date)
    except ValueError:
      print("[X] Invalid date format. Please use DD-MM-YYYY.")
    