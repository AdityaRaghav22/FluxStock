from database.db_semi import insert_semi,get_all_semi,delete_semi_id,edit_name,edit_category,edit_quantity,edit_price,search_semi_db,get_count_semi,product_exists,get_product_id_by_name
from database.db_bom import search_bom_components
from backend.utils import add_semi_sku

def view_semi():
  return get_all_semi()
  
def sales_order_count():
    try:
        return get_count_semi
    except Exception as e:
        print()
        return False, f"[X] Failed to get count: {e}"

def add_semi(name, category, price, quantity):
  sku = add_semi_sku(name, category)
  name = name.title()
  category = category.title()
  price = round(float(price),2)
  quantity = round(float(quantity),2)
  try : 
    if product_exists(prod_name = name):
      prod_id =get_product_id_by_name(name)
      prod_details = search_semi_db(prod_name= name)
      new_quantity  = prod_details[4]+quantity
      edit_semi(prod_id, quantity = new_quantity)
      print(f"[+] Finished Product Updated: {name}")
      return
    insert_semi(name,category,price,quantity,sku)
    print(f"[+] Semi Finished Item Added: {name}")
  except :
    print(f"[X] Failed to add Semi Finished Item material: ")

def del_semi_id(semi_id):
    return delete_semi_id(semi_id)

def edit_semi(semi_id, name=None, category=None, price=None, quantity=None):
  if name:
    edit_name(semi_id,name.title())
  if category:
    edit_category(semi_id,category.title())
  if quantity:
    edit_quantity(semi_id,quantity)
  if price:
    edit_price(semi_id,price)
    
def search_semi(prod_id=None, prod_name=None):
  if prod_id:
    return search_semi_db(prod_id=prod_id)
  elif prod_name:
    return search_semi_db(prod_name=prod_name)
  else:
    return None


def produce_semi_finished(prod_name, qty, unit_price=None):
  from backend.bom import check_bom_completeness, search_bom_components
  from backend.raw_materials import search_raw, edit_quantity as edit_raw_qty
  from backend.semi_finished import (
      search_semi,
      edit_quantity as edit_semi_qty,
      add_semi
  )

  prod_name = prod_name.title()
  existing_product = search_semi(prod_name=prod_name)

  if qty <= 0:
    return False, "[X] Quantity to produce must be greater than zero."

  bom_components_all = search_bom_components(prod_name=prod_name)
  if not bom_components_all or prod_name not in bom_components_all:
    return False, f"[X] No BOM defined for '{prod_name}'. Cannot produce."

  bom_components = bom_components_all[prod_name]
  complete, report = check_bom_completeness(prod_name)
  result_lines = [
    f"{c['component']} → {c['status']} (Req: {c['required']} | Avail: {c['available']})"
    for c in report
  ]
  if not complete:
      result = "\n".join(result_lines)
      return False, f"[X] Insufficient inventory:\n{result}"
  
  for row in bom_components:
    component = row["component"]
    try:
      qty_needed_per_unit = row["quantity"]
    except (ValueError, TypeError):
      print(f"[X] Invalid quantity value in DB: {row.get('quantity')} for component {row.get('component')}")
      continue
    total_required = round(float(qty_needed_per_unit) * qty, 2)
    raw = search_raw(prod_name=component)
    semi = search_semi(prod_name=component)
    if raw and component == raw[1]:
      new_qty = round(raw[4] - total_required, 2)
      if new_qty < 0:
        return False, f"[X] Not enough raw '{component}'"
      edit_raw_qty(raw[0], new_qty)
    elif semi and component == semi[1]:
      new_qty = round(semi[4] - total_required, 2)
      if new_qty < 0:
        return False, f"[X] Not enough semi-finished '{component}'"
      edit_semi_qty(semi[0], new_qty)
    else:
      return False, f"[X] Component '{component}' not found in inventory."
  category = 'Semi'
  total_price = float(unit_price) * qty if unit_price else 0.0
  if existing_product:
    prod_id = existing_product[0]
    new_qty = qty + float(existing_product[4])  # convert Decimal
    edit_semi_qty(prod_id, new_qty)
  else:
    add_semi(prod_name, category, total_price, qty)
  return True, f"[✓] Produced {qty} units of semi-finished '{prod_name}' successfully."
