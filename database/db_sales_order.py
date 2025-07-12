import pymysql
from config import mydb

import datetime
from backend.finished import search_finished



def get_connection():
    return pymysql.connect(**mydb)


def get_count_sales_order():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                select count(order_id)as count from sales_orders;
            """
        )
        row = cursor.fetchone()
        return row[0] if row else 0
    except Exception as e:
        print(f"[X] get_count_sales_orders error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def add_so(order_id,customer_name,order_date,status):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                INSERT INTO sales_orders (order_id,customer_name,order_date,status)
                values(%s,%s,%s,%s)
            """,(order_id,customer_name,order_date,status)
            )
        conn.commit()
        print("[✓] Sales order added successfully.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error add_so error: {e}")
            return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def add_so_item(order_id, product_sku, quantity, unit_price):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO sales_order_items (order_id, product_sku, quantity, unit_price)
            VALUES (%s, %s, %s, %s)
            """,
            (order_id, product_sku, quantity, unit_price)
        )
        conn.commit()
        print(f"[✓] Item added to order {order_id} — SKU: {product_sku}, Qty: {quantity}")
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[X] Error in add_so_item: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_sales_order(order_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                DELETE FROM sales_order_items WHERE order_id = %s
            """,
            (order_id,)
        )
        cursor.execute(
            """
                DELETE FROM sales_orders WHERE order_id = %s
            """,
            (order_id,)
        )
        conn.commit()
        print(f"[✓] Successfully deleted order {order_id} and its items.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[X] Error deleting order {order_id}: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_status(order_id, status):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                update sales_order set status = %s
                where order_id= %s
            """,(status,order_id)
        )
        conn.commit()
        print(f"[✓] Successfully updated order {order_id} to status '{status}'.")
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[X] Error update_staus error: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_recent_orders(limit=5):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT order_id, status, date
            FROM sales_orders
            ORDER BY date DESC
            LIMIT %s;
            """, (limit,)
        )
        rows = cursor.fetchall()
        return {row[0]: f"{row[1]} on {row[2].strftime('%d-%b-%Y %H:%M')}" for row in rows}
    except Exception as e:
        print(f"[X] Error fetching recent orders: {e}")
        return {}
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_order_details(order_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                SELECT
                    so.order_id,
                    so.customer_name,
                    so.order_date,

                    si.item_id,
                    fp.name AS product_name,
                    si.quantity,
                    si.unit_price,
                    (si.quantity * si.unit_price) AS total_item_price
                    
                FROM sales_orders so
                JOIN sales_order_items si ON so.order_id = si.order_id
                JOIN finished fp ON si.product_sku = fp.sku
                WHERE so.order_id = %s
            """,(order_id,)
            )
        
        result = cursor.fetchall()
        return result
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[X] Error update_staus error: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_all_orders():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                SELECT
                    so.order_id,
                    so.customer_name,
                    so.order_date,
                    so.status,

                    si.item_id,
                    si.product_sku,
                    fp.name,
                    si.quantity,
                    si.unit_price,
                    (si.quantity * si.unit_price) AS total_item_price

                FROM sales_orders so
                JOIN sales_order_items si ON so.order_id = si.order_id
                JOIN finished fp ON si.product_sku = fp.sku
                ORDER BY so.order_date DESC;
            """
            )
        
        result = cursor.fetchall()
        return result
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[X] Error get_all_orders error: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
 
def generate_order_id():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
                """
                    SELECT order_id FROM sales_orders ORDER BY order_id DESC LIMIT 1
                """
            )
        result = cursor.fetchone
        if result:
            last_id =result[0]
            last_num = (last_id.replace("ORD", ""))
            new_num = last_num +1
        else:
            new_num = 1
        new_order_id = f"ORD {new_num:03d}"
        return new_order_id
    except Exception as e:
        print(f"[X] Error generating order ID: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
