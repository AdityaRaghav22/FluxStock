import random as r
from backend.utils import add_raw_sku
from database.db_raw import insert_raw,get_all_raw,delete_raw_id,edit_name,edit_category,edit_quantity,edit_price,search_raw_db,get_count_raw


def view_raw():
  return get_all_raw()
  
def sales_order_count():
    try:
        return get_count_raw
    except Exception as e:
        print()
        return False, f"[X] Failed to get count: {e}"

def add_raw(name, category, price, quantity):
  name = name.title()
  category = category.title()
  sku = add_raw_sku(name, category)
  try : 
    price = round(float(price),2)
    quantity = round(float(quantity),2)
    insert_raw(name,category,price,quantity,sku)
    print(f"[+] Raw Material Added: {name}")
    return True
  except :
    print(f"[X] Failed to add raw material: ")
    return False

def del_raw_id(raw_id):
  delete_raw_id(raw_id)

def edit_raw(raw_id, name=None, category=None, price=None, quantity=None):
  if name:
    edit_name(raw_id,name.title())
  if category:
    edit_category(raw_id,category.title())
  if quantity:
    edit_quantity(raw_id,quantity)
  if price:
    edit_price(raw_id,price)
    
def search_raw(prod_id=None, prod_name=None):
  if prod_id:
    return search_raw_db(prod_id=prod_id)
  elif prod_name:
    return search_raw_db(prod_name=prod_name)
  else:
    return None
