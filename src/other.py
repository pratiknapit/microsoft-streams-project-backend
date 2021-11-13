from src.data_store import data_store
from src.data_store import auth_user_id_check, token_to_user_id, is_valid_token
from src.error import InputError, AccessError

def clear_v1():
    store = data_store.get()
    store['users'] = []
    store['channels'] = []
    store['Messages'] = []
    store['dms'] = []
    data_store.set(store)

def notifications_get(token):

    if not is_valid_token(token):
        raise AccessError(description="Not an authorised user invalid")

    user_id = token_to_user_id(token)
    user = auth_user_id_check(user_id)
    
    return {'notifications': user['notifications'][:20]}
