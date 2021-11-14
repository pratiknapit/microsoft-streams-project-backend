from src.error import AccessError, InputError
from src.data_store import auth_user_id_check, data_store, is_valid_token, save_data, token_to_user_id
from src.auth import auth_register_v1
from src.data_store import global_owner_check, remove_user_id_from_channels, remove_user_from_dms



OWNER_PERMISSION = 1
MEMBER_PERMISSION = 2 

def admin_user_remove_v1(token, u_id):
    """
    Need to remove from streams.
    - Need to remove from all channels/DMs

    - Need to remove from list of users.

    
    Streams owners can remove other streams owners (including the original first owner).

    The contents of removed user's messages should be 'Removed users'.

    Their profile must still be retrievable with user/profile, however name_first should be 
    'Removed' and name_last should be 'user'.

    The user's email and handle should be reusable.

    """

    data = data_store.get()

    try:
        int(u_id) 
        it_is = True
    
    except ValueError:
        it_is = False
    
    if it_is == False:
        raise InputError("Invalid Auth Input")

    if not is_valid_token(token):
        raise AccessError(description="not an authorised user")
    
    if not auth_user_id_check(u_id):
        raise InputError("U_id does not refer to a valid user")

    if global_owner_check(u_id):
        raise InputError("U_id refers to a user who is the only global owner.")
    
    auth_user = token_to_user_id(token)

    if not global_owner_check(auth_user):
        raise InputError("The authorised user is not a global owner.")

    #Add a is_removed key for the user so that user/all and user/profile returns correctly

    for user in data['users']:
        if user['u_id'] == u_id: 
            user['name_first'] = "Removed"
            user['last_name'] = "user"
            user['is_removed '] = True
            if user['permission_id'] == 1:
                user['permission_id'] == 2
            
            break
    
    remove_user_id_from_channels(u_id)

    remove_user_from_dms(u_id)

    save_data(data)
    return {}

    

def admin_user_permission_change_v1(token, u_id, permission_id): 

    data = data_store.get()

    #token check 
    if not is_valid_token(token):
        raise AccessError(description="not an authorised user")

    if not auth_user_id_check(u_id):
        raise InputError("U_id does not refer to a valid user.")
    
    if permission_id != OWNER_PERMISSION and permission_id != MEMBER_PERMISSION:
        raise InputError("Permission_id is invalid")

    user_id = token_to_user_id(token) 
    auth_user = auth_user_id_check(user_id)

    for user in data['users']:
        if user['u_id'] == auth_user['u_id']:
            auth_user_permissions = user['permission_id']
            break 
    
    if auth_user_permissions != OWNER_PERMISSION:
        raise AccessError("The authorised user is not a global owner.")
    
    for user in data['users']:
        if user['u_id'] == u_id:
            user['permission_id'] = permission_id
            break 
    
    save_data(data)

    return {}

"""
if __name__ == '__main__':
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'passworddd', 'Alpha', 'BB')
    admin_user_permission_change_v1(dummy_user_1['token'], dummy_user_2['auth_user_id'], OWNER_PERMISSION)
"""

