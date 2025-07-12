from database.db_finished import insert_finished,get_all_finished,delete_finished_id,edit_name,edit_category,edit_quantity,edit_price,search_finished_db,get_count_finished
from backend.raw_materials import search_raw, edit_quantity as edit_raw_qty
from database.db_bom import search_bom_components
from backend.utils import add_finished_sku

def view_finished():
  return get_all_finished()

def finished_count():
    try:
        return get_count_finished
    except Exception as e:
        print()
        return False, f"[X] Failed to get count: {e}"

def add_finished(name, category, price, quantity):
  sku = add_finished_sku(name, category)
  name = name.title()
  category = category.title()
  price = round(float(price),2)
  quantity = round(float(quantity),2)
  try : 
    insert_finished(name,category,price,quantity,sku)
    print(f"[+] Finished Product Added: {name}")
  except :
    print(f"[X] Failed to add Finished Product ")

def del_finished_id(finished_id):
    delete_finished_id(finished_id)

def edit_finished(finished_id, name=None, category=None, price=None, quantity=None):
  if name:
    edit_name(finished_id,name.title())
  if category:
    edit_category(finished_id,category.title())
  if quantity:
    edit_quantity(finished_id,quantity)
  if price:
    edit_price(finished_id,price)
    
def search_finished(prod_id=None, prod_name=None):
    if prod_id:
        return search_finished_db(prod_id=prod_id)
    elif prod_name:
        return search_finished_db(prod_name=prod_name)
    else:
        return None

def produce_finished(prod_name, qty, unit_price=None):
  from backend.bom import check_bom_completeness
  from backend.semi_finished import search_semi, edit_quantity as edit_semi_qty
  from backend.raw_materials import search_raw, edit_quantity as edit_raw_qty
  from backend.finished import search_finished, edit_quantity as edit_finished, add_finished
  from backend.bom import search_bom_components
  prod_name = prod_name.title()
  existing_product = search_finished(prod_name=prod_name)
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
  category = 'Finished'
  total_price = float(unit_price) * qty if unit_price else 0.0
  if existing_product:
    prod_id = existing_product[0]
    new_qty = qty + float(existing_product[4])
    edit_finished(prod_id, quantity=new_qty)
  else:
    add_finished(prod_name, category, total_price, qty)
  return True, f"[✓] Produced {qty} units of '{prod_name}' successfully."