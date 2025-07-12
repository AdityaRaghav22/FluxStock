import pymysql
from config import mydb



def get_connection():
    return pymysql.connect(**mydb)

def insert_user(username,first_name, last_name, email, hashed_pw):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO users (username,first_name, last_name, email, password_hash)
            VALUES (%s, %s, %s, %s,%s)
        """, (username,first_name, last_name, email, hashed_pw))
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"[X] Error insert_user error: {e}")
    finally:
        if cursor:cursor.close()
        if conn:conn.close()

def del_user_name(username):
    conn = None 
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username = %s", (username,))
        conn.commit()
        return cursor.rowcount > 0  
    except Exception as e:
        conn.rollback()
        print(f"Error deleting by username: {e}")
        return False
    finally:
        if cursor:cursor.close()
        if conn:conn.close()

def del_user_emailid(email):
    conn = None 
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE email = %s", (email,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"Error deleting by email: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def search_user(username=None, email=None):
    conn = None 
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if username:
            cursor.execute(
                """
                    select username,first_name,last_name,email from users
                    where username = %s
                """,(username,)
            )
        elif email:
            cursor.execute(
                """
                    select username,first_name,last_name,email from users
                    where email = %s
                """,(email,)
            )
        else:
            return None
        result = cursor.fetchone()
        return result
    except Exception as e:
        print(f"[X] search_user error: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_user_password_username(username = None , email = None):
    conn = None 
    cursor = None
    if username:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                    select username, password_hash from users
                    where username = %s 
                """,(username,)
            )
            result = cursor.fetchone()
            return result    
        except Exception as e:
            print(f"[X] Error fetching user for login: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    if email:
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(
                """
                    select email, password_hash from users
                    where email = %s 
                """,(email,)
            )
            result = cursor.fetchone()
            return result    
        except Exception as e:
            print(f"[X] Error fetching user for login: {e}")
            return None
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    
def get_user_password_email(email):
    conn = None 
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                select username, password_hash from users
                where email = %s
            """,(email,)
            )
        result = cursor.fetchone()
        return result    
    except Exception as e:
        print(f"[X] Error fetching user for login: {e}")
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def update_password(email,new_hashed_pw):
    conn = None 
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
                update users set password_hash = %s 
                where email = %s
            """,(new_hashed_pw,email)
        )
        conn.commit()
        return cursor.rowcount > 0
    except Exception as e:
        conn.rollback()
        print(f"[X] Error updating password: {e}")
        return False
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def get_all_users():
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT username, first_name, last_name, email FROM users")
        return cursor.fetchall()
    except Exception as e:
        print(f"[X] get_all_users error: {e}")
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()
