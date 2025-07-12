import pymysql
from config import mydb


def get_connection():
    return pymysql.connect(**mydb)

def get_max_product_id():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT MAX(product_id) FROM bom")
    result = cursor.fetchone()
    return result[0] if result[0] is not None else 0

def get_product_id_by_name(prod_name):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_id
            FROM bom
            WHERE product_name = %s
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

def get_product_name_by_id(prod_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_name
            FROM bom
            WHERE product_id = %s
            LIMIT 1
        """, (prod_id,))
        row = cursor.fetchone()
        return row[0] if row else None

    except Exception as e:
        print(f"[X] Error in get_product_name_by_id: {e}")
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
                SELECT 1 FROM bom
                WHERE product_id = %s OR product_name = %s
                LIMIT 1
            """, (prod_id, prod_name))
        elif prod_id is not None:
            cursor.execute("""
                SELECT 1 FROM bom
                WHERE product_id = %s
                LIMIT 1
            """, (prod_id,))
        elif prod_name is not None:
            cursor.execute("""
                SELECT 1 FROM bom
                WHERE product_name = %s
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

def add_bom_db(prod_id,prod_name,comp_name,comp_qty):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                insert INTO bom (product_id,product_name,component_name,quantity)
                values (%s,%s,%s,%s)
            """,(prod_id,prod_name,comp_name,comp_qty)
        )
        conn.commit()
        print(f"[+] Component '{comp_name}' added to BOM for Product ID {prod_id}")
        return True
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"[X] Error insert_bom_comp error: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_component(prod_id,comp_name):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                DELETE FROM bom
                WHERE product_id = %s AND component_name = %s;
            """,(prod_id,comp_name)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            print(f"[X] Error delete_component error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def search_bom_components(prod_id=None, prod_name=None):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if prod_id is not None and prod_name is not None:
            cursor.execute("""
                SELECT product_name, component_name, quantity
                FROM bom
                WHERE product_id = %s OR product_name = %s
            """, (prod_id, prod_name))
        elif prod_id is not None:
            cursor.execute("""
                SELECT product_name, component_name, quantity
                FROM bom
                WHERE product_id = %s
            """, (prod_id,))
        elif prod_name is not None:
            cursor.execute("""
                SELECT product_name, component_name, quantity
                FROM bom
                WHERE product_name = %s
            """, (prod_name,))
        else:
            return {}

        result = cursor.fetchall()
        bom_dict = {}

        for row in result:
            prod = row[0]
            component = row[1]
            qty = row[2]
            try:
                qty = float(qty)
            except (ValueError, TypeError):
                print(f"[X] Invalid quantity value in DB: {qty} for component {component}")
                continue

            if prod not in bom_dict:
                bom_dict[prod] = []
            bom_dict[prod].append({
                "component": component,
                "quantity": qty
            })

        return bom_dict

    except Exception as e:
        print(f"[X] Error in search_bom_components: {e}")
        return {}
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_all_bom():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                SELECT product_name,component_name,quantity
                FROM bom 
            """
        )
        result = cursor.fetchall()
        bom_dict = {}
        for row in result:
            product = row[0]
            component = row[1]
            qty = row[2]
            if product not in bom_dict:
                bom_dict[product] = []
            bom_dict[product].append({
                "component": component,
                "quantity": qty
            })
        return bom_dict
    except Exception as e:
        if conn:
            print(f"[X] Error get_all_bom error: {e}")
            return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def edit_component(new_name, prod_id, comp_name):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                update bom set component_name = %s 
                where product_id = %s and component_name= %s
            """,(new_name, prod_id, comp_name)
        )
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error edit_component error: {e}")
            return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def edit_qty(qty,prod_id,comp_name):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                update bom set quantity = %s
                where product_id = %s and component_name = %s
            """,(qty,prod_id,comp_name)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            conn.rollback()
            print(f"[X] Error edit_component error: {e}")
            return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def delete_bom_db(prod_id):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                DELETE FROM bom
                WHERE product_id = %s 
            """,(prod_id,)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        if conn:
            print(f"[X] Error delete_component error: {e}")
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
