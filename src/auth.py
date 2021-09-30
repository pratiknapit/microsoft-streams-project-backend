###########
#Functions#
###########
from data_store import data_store, add_user, make_user, create_handle 

##########################
# Helper Check Functions #
##########################
from data_store import email_check, email_repeat_check, handle_check, auth_user_id_check, password_check

###################
# Error Functions #
###################
from error import InputError

def auth_login_v1(email, password):
    if not email_check(email): 
        raise InputError
    if not email_repeat_check(email):
        raise InputError
    if not password_check(password):
        raise InputError

    cur_user = login_email(email) 
    return {
        "auth_user_id": cur_user["auth_user_id"],
    }

def auth_register_v1(email, password, name_first, name_last):                     # Add_user

    if email_check(email) == False:
        raise InputError
    if email_repeat_check(email) == True:
        raise InputError
    if len(password) < 6:
        raise InputError
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError

    added_user = add_user(email, password, name_first, name_last)
    return {
        "auth_user_id": added_user["auth_user_id"],
    }
