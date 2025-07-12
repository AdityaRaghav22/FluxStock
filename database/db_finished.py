import pymysql
from config import mydb



def get_connection():
    return pymysql.connect(**mydb)

def get_product_id_by_name(prod_name):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id
            FROM finished
            WHERE name = %s
            LIMIT 1
        """, (prod_name,))
        row = cursor.fetchone()
        return row[0] if row else None

    except Exception as e:
        print(f"[X] Error in get_product_id_by_name: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def product_exists(prod_id=None, prod_name=None):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if prod_id is not None and prod_name is not None:
            cursor.execute("""
                SELECT 1 FROM finished
                WHERE id = %s OR name = %s
                LIMIT 1
            """, (prod_id, prod_name))
        elif prod_id is not None:
            cursor.execute("""
                SELECT 1 FROM finished
                WHERE id = %s
                LIMIT 1
            """, (prod_id,))
        elif prod_name is not None:
            cursor.execute("""
                SELECT 1 FROM finished
                WHERE name = %s
                LIMIT 1
            """, (prod_name,))
        else:
            return False
        return cursor.fetchone() is not None
    except Exception as e:
        print(f"[X] Error in product_exists: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_count_finished():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                select count(id)as count from finished;
            """
        )
        row = cursor.fetchone()
        return row[0] if row else 0
    except Exception as e:
        print(f"[X] get_count_finished error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_all_finished():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category, price, quantity, sku FROM finished")
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
        print(f"[X] get_all_finished error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_finished_skus():
    conn = None
    cursor = None
    try:    
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""select sku from finished""")
        skus = [row[0] for row in cursor.fetchall()]
        return skus
    except Exception as e:
        print(f"[X] get_finished_skus error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def search_finished_db(prod_id=None, prod_name=None):
    conn = None
    cursor = None 
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if prod_id:
            cursor.execute(
                """
                    select id,name,category,price,quantity,sku from finished
                    where id = %s
                """,(prod_id,)
        )
        elif prod_name:
            cursor.execute(
                """
                    select id,name,category,price,quantity,sku from finished
                    where name = %s
                """,(prod_name.title(),)
        )
        else:
            return None   
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"[X] search_finished_db error: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def insert_finished(name, category, price, quantity, sku):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                INSERT INTO finished (name, category, price, quantity, sku)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, category, price, quantity, sku))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error insert_finished error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_finished_id(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                DELETE from finished where id = %s
            """, (id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error delete_finished_id error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def edit_finished_all(prod_id, name, category, price, quantity):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                UPDATE finished
                SET name = %s, category = %s, price = %s, quantity = %s
                WHERE id = %s
            """, (name, category, price, quantity, prod_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error update_finished_all error: {e}")
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
                update finished set name = %s where id = %s 
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
                update finished set category = %s where id = %s 
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
                update finished set quantity = %s where id = %s 
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
                update finished set price = %s where id = %s 
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