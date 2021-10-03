###########
#Functions#
###########
from src.data_store import data_store, add_user, make_user, create_handle, login_email

##########################
# Helper Check Functions #
##########################
from src.data_store import email_check, email_repeat_check, handle_check, auth_user_id_check, password_check

###################
# Error Functions #
###################
from src.error import InputError

def auth_login_v1(email, password):
    if not email_check(email): 
        raise InputError
    if not email_repeat_check(email):
        raise InputError
    if not password_check(password):
        raise InputError

    cur_user = login_email(email) 
    return {
        "auth_user_id": cur_user["u_id"],
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
        "auth_user_id": added_user["u_id"],
    }

if __name__ == '__main__':

    dummy_user_1 = add_user('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'Napit')
    dummy_user_2 = add_user('dummyuser2@gmail.com', 'yessword', 'Alpha', 'Napit')
    dummy_user_3 = add_user('dummyuser3@gmail.com', 'passsssword', 'Alpha', 'Napit')
    print(dummy_user_1) 
    print(dummy_user_2)
    print(dummy_user_3)
