
from src.data_store import data_store, add_user, make_user, create_handle 

##########################
# Helper Check Functions #
##########################
from src.data_store import email_check, handle_check

###################
# Error Functions #
###################
from src.error import InputError

#def get_user_store():
 #   global data_store.get()
 #   return data_store.get()




def auth_login_v1(email, password):
    return {
        'auth_user_id': 1,
    }



def auth_register_v1(email, password, name_first, name_last):                     # Add_user

    if email_check(email) == False:
        raise InputError
#    if email_repeat_check(email) == True:
#        raise InputError
    if len(password) < 6:
        raise InputError
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError

    added_user = add_user(email, password, name_first, name_last)
 #   data = data_store.get()
 #   for i in data['users']:
 #       if i['u_id'] == added_user['u_id']:
 #           i['token'] = token
    users = data_store.get()
    print(users)
    return {
        "auth_user_id": added_user["u_id"],
    }
