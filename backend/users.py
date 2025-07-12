from werkzeug.security import generate_password_hash, check_password_hash
from database.db_users import insert_user,del_user_emailid,del_user_name,search_user,get_user_password_username,get_user_password_email,update_password

def add_user(username,first_name,last_name,email,password):
    hashed_pw = generate_password_hash(password)
    fname = first_name.title()
    lname = last_name.title()
    if "@" in email and ".com" in email:
        valid_email = email

    else:
        return False
    
    insert_user(username,fname,lname,valid_email,hashed_pw)
    return True

def delete_user(username=None, email=None):
    if username:
        return del_user_name(username)
    elif email:
        return del_user_emailid(email)
    else:
        return False
    
def is_registered(username=None,email=None):
    user = search_user(username=username, email=email)
    if user:
        return True
    else:
        print("No user found")
        return False
    
def get_user_info(username=None,email=None):
    user_data = search_user(username=username, email=email)
    if user_data: 
        user_info = {"user_name" : user_data[0],
                    "first_name": user_data[1],
                    "lastname": user_data[2],
                    "user_email": user_data[3]}
        return user_info
        
    else:
        print("No user found")
        return {}
    
def verify_user(input_password,username = None,email=None):
    if username:
        user = get_user_password_username(username)
    elif username:
        user = get_user_password_email(username)
    else:
        return
    if user:
        stored_hash = user[1]
        check = check_password_hash(stored_hash, input_password)
    else:
        print("No user found")
        return False
    if check:
        return user
    else:
        return False

def reset_password(username, email, old_password, new_password):
    if not verify_user(username, old_password):
        print("Old password is incorrect")
        return False
    new_hashed_pw = generate_password_hash(new_password)
    success = update_password(email, new_hashed_pw)
    if success:
        print("Password updated successfully")
    else:
        print("Failed to update password")
    return success
