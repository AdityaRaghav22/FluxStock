from backend.raw_materials import search_raw
from database.db_bom import search_bom_components,add_bom_db,delete_component,get_all_bom,edit_component,edit_qty,delete_bom_db,product_exists,get_product_id_by_name,get_max_product_id

# [X] Invalid quantity value in DB: 

def add_bom_components(prod_name, comp_name, qty):
    prod_name = prod_name.title()
    comp_name = comp_name.title()
    try:
        qty = round(float(qty), 2)
    except ValueError:
        return False, "[X] Invalid quantity"
    try:
        if product_exists(prod_name=prod_name):
            prod_id = get_product_id_by_name(prod_name)
        else:
            prod_id = get_max_product_id() + 1
        add_bom_db(prod_id, prod_name, comp_name, qty)
        return True, f"[+] BOM component '{comp_name}' added to '{prod_name}' (Product ID: {prod_id})"
    except Exception as e:
        return False, f"[X] Failed to add BOM: {e}"

def delete_bom_component(prod_name, comp_name):
    prod_name = prod_name.title()
    comp_name = comp_name.title()
    try:
        prod_id = get_product_id_by_name(prod_name)
        deleted = delete_component(prod_id, comp_name)
        if deleted:
            return True, f"[✓] BOM component '{comp_name}' deleted for product '{prod_name}'"
        else:
            return False, f"[!] Component '{comp_name}' not found in BOM for '{prod_name}'"
    except Exception as e:
        return False, f"[X] Failed to delete BOM for Product '{prod_name}': {e}"

def update_bom_component(prod_name, comp_name, new_name=None, qty=None):
  prod_name = prod_name.title()
  comp_name = comp_name.title()
  try:
    prod_id = get_product_id_by_name(prod_name)
  except Exception as e:
    return False, f"[X] Could not find product ID for '{prod_name}': {e}"
  if qty is not None:
    try:
      qty = round(float(qty), 2)
      updated = edit_qty(prod_id, comp_name, qty)
      if updated:
        return True, f"[✓] Quantity for '{comp_name}' updated to {qty}"
      else:
        return False, f"[!] Component '{comp_name}' not found in BOM"
    except Exception as e:
      return False, f"[X] Failed to update quantity: {e}"
  if new_name is not None:
    new_name = new_name.title()
    try:
      updated = edit_component(prod_id, comp_name, new_name)
      if updated:
        return True, f"[✓] Component '{comp_name}' renamed to '{new_name}'"
      else:
        return False, f"[!] Component '{comp_name}' not found in BOM"
    except Exception as e:
      return False, f"[X] Failed to update component name: {e}"
  return False, "[X] No update performed — missing 'qty' or 'new_name'"

def get_bom(prod_name):
  prod_name = prod_name.title()
  try:
    prod_id = get_product_id_by_name(prod_name)
    bom = search_bom_components(prod_id=prod_id)
    if not bom or prod_name not in bom:
      return False, {}
    return True, {prod_name: bom[prod_name]}  # Return only selected product BOM
  except Exception as e:
      print(f"[X] Failed to get BOM for '{prod_name}': {e}")
      return False, {}

def get_all_boms():
  try:
    all_bom = get_all_bom()
    if not all_bom:
      print("[!] No BOMs found.")
      return False, {}

    return True, all_bom
  except Exception as e:
    print(f"[X] Failed to retrieve all BOMs: {e}")
    return False, {}

def check_bom_completeness(prod_name):
  from backend.semi_finished import search_semi

  prod_name = prod_name.title()
  try:
    prod_id = get_product_id_by_name(prod_name)
  except Exception as e:
    return False, f"[X] Failed to get product ID: {e}"
  complete = True
  completeness_report = []
  try:
    components_details = search_bom_components(prod_id=prod_id)
    if not components_details or prod_name not in components_details:
      return False, f"[X] No BOM found for product '{prod_name}'"
    components = components_details[prod_name]
  except Exception as e:
    return False, f"[X] Failed to fetch components: {e}"
  for row in components:
    component = row["component"]
    qty_needed = row["quantity"]

    available = 0
    try:
      raw_detail = search_raw(prod_name=component)
      if raw_detail and component == raw_detail[1]:
        available += raw_detail[4]
    except Exception as e:
      return False, f"[X] Error checking raw: {e}"
    try:
      semi_detail = search_semi(prod_name=component)
      if semi_detail and component == semi_detail[1]:
        available += semi_detail[4]
    except Exception as e:
      return False, f"[X] Error checking semi-finished: {e}"
    if available == 0:
      completeness_report.append({
        "component": component,
        "status": "❌ Missing",
        "required": qty_needed,
        "available": 0
      })
      complete = False
    else:
      status = "✅ Sufficient" if available >= qty_needed else "❌ Insufficient"
      completeness_report.append({
        "component": component,
        "status": status,
        "required": qty_needed,
        "available": available
      })
      if available < qty_needed:
        complete = False
  return complete, completeness_report

def delete_bom(prod_name):
    try:
        prod_id = get_product_id_by_name(prod_name.title())
        delete_bom_db(prod_id)
        return True, f"BOM deleted for Product: {prod_name}"
    except Exception as e:
        return False, f"[X] Failed to delete BOM for Product '{prod_name}': {e}"
