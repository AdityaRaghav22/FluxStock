
from datetime import datetime
from database.db_sales_order import add_so,add_so_item,delete_sales_order,get_order_details,get_all_orders,generate_order_id,update_status,get_count_sales_order,get_recent_orders

sales_order_status = {"Pending", "Processing", "Shipped","Delivered","Cancelled"}
def view_all_sales_orders():
    try:
        return get_all_orders()
    except Exception as e:
        print()
        return False, f"[X] Failed to view orders: {e}"

def view_sales_order(order_id):
    try:
        return get_order_details(order_id)
    except Exception as e:
        return False, f"[X] Failed to view order with id: {order_id} :{e} "

def get_recent_sales_order():
    try:
        return get_recent_orders()
    except Exception as e:
        return False, f"[X] Failed to view recent order: {e} "


def sales_order_count():
    try:
        return int(get_count_sales_order)
    except Exception as e:
        print()
        return False, f"[X] Failed to get count: {e}"

def add_sales_order(customer_name, item_dict, order_date=None):
    from backend.finished import search_finished,edit_finished
    order_id = generate_order_id()
    total_price = 0.0

    if order_date is None:  
        order_date = datetime.now()

    # 1. Validate items
    for prod_name, qty in item_dict.items():
        prod_name = prod_name.title()
        prod_detail = search_finished(prod_name)
        if not prod_detail:
            return False, f"[X] Product '{prod_name}' not found in finished table."
        stock = prod_detail[4]  #
        if stock is None or stock < qty:
            return False, f"[X] Not enough stock for '{prod_name}'. Requested: {qty}, Available: {stock}"

    try:
        # 2. Add sales order to DB
        if not add_so(order_id, customer_name, order_date, "pending"):
            return False, "[X] Failed to create sales order."

        # 3. Add items to sales_order_items and update stock
        for prod_name, qty in item_dict.items():
            prod_name = prod_name.title()
            prod_detail = search_finished(prod_name)
            sku = prod_detail[5]
            unit_price = prod_detail[3]
            add_so_item(order_id, sku, qty, unit_price)
            finished_qty = prod_detail[4] - qty
            edit_finished(prod_detail[0],quantity = finished_qty )
            total_price += qty * unit_price

        return True, total_price , f"[✓] Sales order '{order_id}' placed for '{customer_name}'. Total: ₹{total_price:.2f}"

    except Exception as e:
        print(f"[X] Failed to add sales order for '{customer_name}': {e}")
        return False, f"[X] Error occurred: {e}"
    
def delete_order(order_id):
    try:
        delete_sales_order(order_id)
        return True, f"[✓] Sales order '{order_id}' deleted successfully"
    except Exception as e:
        print(f"[X] Failed to delete sales order for order_id: '{order_id}': {e}")
        return False, f"[X] Error occurred: {e}"

def update_sales_order_status(order_id, new_status):
    try:
        update_status(order_id,new_status)
        return True, f"[✓] Sales order '{order_id}' updated successfully"
    except Exception as e:
        print(f"[X] Failed to update sales order for order_id: '{order_id}': {e}")
        return False, f"[X] Error occurred: {e}"





