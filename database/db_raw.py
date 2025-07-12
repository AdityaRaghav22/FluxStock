import pymysql
from config import mydb



def get_connection():
    return pymysql.connect(**mydb)

def get_count_raw():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                select count(id)as count from raw;
            """
        )
        row = cursor.fetchone()
        return row[0] if row else 0
    except Exception as e:
        print(f"[X] get_count_raw error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_all_raw():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category, price, quantity, sku FROM raw")
        rows = cursor.fetchall()
        return {
        name: {
            "id": id_,
            "category": category,
            "quantity": qty,
            "price": price,
            "sku": sku
        }for id_, name, category, price, qty, sku in rows
    }
    except Exception as e:
        print(f"[X] get_all_raw error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_raw_skus():
    conn = None
    cursor = None
    try:    
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""select sku from raw""")
        skus = [row[0] for row in cursor.fetchall()]
        return skus
    except Exception as e:
        print(f"[X] get_raw_skus error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_raw_name():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""select name from raw""")
        names = [row[0] for row in cursor.fetchall()]
        return names
    except Exception as e:
        print(f"[X] get_raw_name error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def search_raw_db(prod_id=None, prod_name=None):
    conn = None
    cursor = None 
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if prod_id:
            cursor.execute(
                """
                    select id,name,category,price,quantity,sku from raw
                    where id = %s
                """,(prod_id,)
        )
        elif prod_name:
            cursor.execute(
                """
                    select id,name,category,price,quantity,sku from raw
                    where name = %s
                """,(prod_name.title(),)
        )
        else:
            return None   
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"[X] search_raw_db error: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def insert_raw(name, category, price, quantity, sku):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                INSERT INTO raw (name, category, price, quantity, sku)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, category, price, quantity, sku)
            )
        conn.commit()
    except Exception as e:
        if conn:
            {}
            print(f"[X] Error insert_raw error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_raw_id(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                DELETE from raw where id = %s
            """, (id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error delete_raw_id error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_raw_all(prod_id, name, category, price, quantity):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                UPDATE raw
                SET name = %s, category = %s, price = %s, quantity = %s
                WHERE id = %s
            """, (name, category, price, quantity, prod_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] update_raw_all error: {e}")
            return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def edit_name(prod_id,name):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                update raw set name = %s where id = %s 
            """,(name,prod_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error edit_name error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def edit_category(prod_id,category):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                update raw set category = %s where id = %s 
            """,(category,prod_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error edit_category error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    
def edit_quantity(prod_id,quantity):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                update raw set quantity = %s where id = %s 
            """,(quantity,prod_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error edit_quantity error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
    
def edit_price(prod_id,price):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                update raw set price = %s where id = %s 
            """,(price,prod_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error edit_price error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
