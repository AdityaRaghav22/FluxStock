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
            FROM semi
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
                SELECT 1 FROM semi
                WHERE id = %s OR name = %s
                LIMIT 1
            """, (prod_id, prod_name))
        elif prod_id is not None:
            cursor.execute("""
                SELECT 1 FROM semi
                WHERE id = %s
                LIMIT 1
            """, (prod_id,))
        elif prod_name is not None:
            cursor.execute("""
                SELECT 1 FROM semi
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

def get_count_semi():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                select count(id)as count from semi;
            """
        )
        row = cursor.fetchone()
        return row[0] if row else 0
    except Exception as e:
        print(f"[X] get_count_semi error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_all_semi():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, category, price, quantity, sku FROM semi")
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
        print(f"[X] get_all_semi error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_semi_skus():
    conn = None
    cursor = None
    try:    
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""select sku from semi""")
        skus = [row[0] for row in cursor.fetchall()]
        return skus
    except Exception as e:
        print(f"[X] get_semi_skus error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_semi_name():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""select name from semi""")
        names = [row[0] for row in cursor.fetchall()]
        return names
    except Exception as e:
        print(f"[X] get_semi_name error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def search_semi_db(prod_id=None, prod_name=None):
    conn = None
    cursor = None 
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if prod_id:
            cursor.execute(
                """
                    select id,name,category,price,quantity,sku from semi
                    where id = %s
                """,(prod_id,)
        )
        elif prod_name:
            cursor.execute(
                """
                    select id,name,category,price,quantity,sku from semi
                    where name = %s
                """,(prod_name.title(),)
        )
        else:
            return None   
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"[X] search_semi_db error: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def insert_semi(name, category, price, quantity, sku):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                INSERT INTO semi (name, category, price, quantity, sku)
                VALUES (%s, %s, %s, %s, %s)
            """, (name, category, price, quantity, sku))
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error insert_semi error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_semi_id(id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                DELETE from semi where id = %s
            """, (id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error delete_semi_id error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_semi_all(prod_id, name, category, price, quantity):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                UPDATE semi
                SET name = %s, category = %s, price = %s, quantity = %s
                WHERE id = %s
            """, (name, category, price, quantity, prod_id)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] update_semi_all error: {e}")
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
                update semi set name = %s where id = %s 
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
                update semi set category = %s where id = %s 
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
                update semi set quantity = %s where id = %s 
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
                update semi set price = %s where id = %s 
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
