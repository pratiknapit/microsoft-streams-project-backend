from src.data_store import data_store
from src.data_store import hash_password
import random
import string

##############
#auth helpers#
##############
def token_logout(token):
    store = data_store.get()
    for user in store['users']:
        if user['token'] == token:
            user.pop('token')
            return True
    return False

def generate_reset_code(email):
    data = data_store.get()
    for user in data['users']:
        if user['email'] == email:
            reset_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            user['reset_code'] = reset_code
            return reset_code

def change_password(reset_code, new_password):
    data = data_store.get()
    found = False
    for user in data['users']:
        if user['reset_code'] == reset_code:
            user['password'] = hash_password(new_password)
            user['reset_code'] = 0
            found = True
            return found
    return found

###########
#dm helper#
###########

def list_dm(dm_list, decoded_token):
    data = data_store.get()
    for dm in data['dms']:
        for member in dm['members']:
            if member == decoded_token['auth_user_id']:
                dm_list.append({'dm_id': dm['dm_id'],
                                'name': dm['name']})
                return dm_list