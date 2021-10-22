import sys
import signal
from json import dumps
from flask import Flask, request
from src.channel import channel_add_owner_v2, channel_join_v1, channel_details_v1, channel_leave_v2
from src.channel import channel_remove_owner_v2, channel_invite_v1, channel_messages_v1
from flask_cors import CORS
from src.error import InputError
from src import config
from src.channels import channels_create_v1, channels_list_v1, channels_listall_v1
from src.data_store import password_check, email_check, email_repeat_check
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1, auth_logout
from src.message import message_send, message_edit, message_remove
from src.user import user_profile_v1, user_profile_setname_v1, user_profile_setemail_v1
from src.user import user_profile_sethandle_v1, users_all_v1
from src.dm import dm_create, dm_list, dm_remove, dm_details, dm_leave, dm_messages

def quit_gracefully(*args):
    '''For coverage'''
    exit(0)

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

#### NO NEED TO MODIFY ABOVE THIS POINT, EXCEPT IMPORTS

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
   	    raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

@APP.route("/clear/v1", methods=["DELETE"])
def clear():
    clear_v1()
    return dumps({})

@APP.route("/auth/register/v2", methods=["POST"])
def register_auth():
    data = request.get_json()

    email = data["email"]
    password = data["password"]
    name_first = data["name_first"]
    name_last = data["name_last"]

    if not email_check(email):
        raise InputError(description="Email not valid")
    if email_repeat_check(email):
        raise InputError(description="Email already used")
    if len(password) < 6:
        raise InputError(description="Password less than 6 characters")
    if len(name_first) < 1 or len(name_first) > 50:
        raise InputError(description="First name is invalid")
    if len(name_last) < 1 or len(name_last) > 50:
        raise InputError(description="Last name is invalid")

    user = auth_register_v1(email, password, name_first, name_last)
    auth_uid = user['auth_user_id']
    auth_token = user['token']
    
    return dumps({
        'auth_user_id': auth_uid,
        'token': auth_token,
    })

@APP.route("/auth/login/v2", methods=["POST"])
def login_auth():
    data = request.get_json()

    email = data["email"]
    password = data["password"]

    if not email_check(email):
        raise InputError(description="Email not valid")
    if not email_repeat_check(email):
        raise InputError(description="Email already used")
    if not password_check(password):
        raise InputError(description="Password incorrect")

    login_info = auth_login_v1(email, password)
    u_id = login_info['auth_user_id']
    new_token = login_info['token']

    return dumps({
        "auth_user_id": u_id,
        "token": new_token,
    })

@APP.route("/auth/logout/v1", methods=["POST"])
def logout_auth():
    data = request.get_json()
    token = data["token"]
    result = auth_logout(token)

    return dumps({
        'is_success': result
    })


#Channels HTTP Server Wrappers

@APP.route("/channels/create", methods=['POST'])
def channels_create_v2():
    """
    This is a flask wrapper for the channels_create function.  
    """
    data = request.get_json()
    token = data['token']
    name = data['name']
    is_public = data['is_public']
    channel_id = channels_create_v1(token, name, is_public)

    return dumps(channel_id)

@APP.route("/channels/list", methods=['GET'])
def channels_list_v2():
    """
    This is a flask wrapper for the channels_list function.  
    """
    
    #no input for channels_list 
    token = request.args.get('token')
    #token = int(token)
    #need to add a token check
    
    return_channel_list = channels_list_v1(token)
    return dumps(return_channel_list)

@APP.route("/channels/listall", methods=['GET'])
def channels_list_all_v2():
    """
    This is a flask wrapper for the channels_list function.  
    """
    
    #no input for channels_list 
    token = request.args.get('token')
    #token = int(token)
    #need to add a token check
    
    return_channel_list_all = channels_listall_v1(token)
    return dumps(return_channel_list_all)

@APP.route("/channels/details", methods=['GET'])
def c_details_v2():
    """
    This is a flask wrapper for the channels_details function.  
    """
    token = request.args.get('token')
    channel_id = request.args.get('channel_id') 
    
    #need to add a token check and channel id check, assume for now they are valid.

    return_dict = channel_details_v1(token, channel_id)
    return dumps(return_dict)

@APP.route("/channels/join", methods=['POST'])
def channel_join_v2():
    """
    This is a flask wrapper for the channels_create function.  
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    #do token and channel_id checks 
    return dumps(channel_join_v1(token, channel_id))

@APP.route("/channel/leave", methods=['POST'])
def c_leave_v2():
    """
    This is a flask wrapper for the channels_create function.  
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    #do token and channel_id checks 
    return dumps(channel_leave_v2(token, channel_id))

@APP.route("/channel/addowner", methods=['POST'])
def c_addowner_v2():
    """
    This is a flask wrapper for the channels_create function.  
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    #do token and channel_id checks 
    channel_add_owner_v2(token, channel_id, u_id)
    return dumps({})

@APP.route("/channel/removeowner", methods=['POST'])
def c_removeowner_v2():
    """
    This is a flask wrapper for the channels_create function.  
    """
    data = request.get_json()
    token = data['token']
    channel_id = data['channel_id']
    u_id = data['u_id']
    #do token and channel_id checks 
    channel_remove_owner_v2(token, channel_id, u_id)
    return dumps({})

@APP.route("/channel/invite/v2", methods=['POST'])
def c_invite():
    data = request.get_json()
    token = data['token']
    channel_id = int(data['channel_id'])
    u_id = int(data['u_id'])

    out = channel_invite_v1(token, channel_id, u_id)
    return dumps(out)

@APP.route("/channel/messages/v2", methods=['GET'])
def c_messages():
    
    token = request.args.get('token')
    channel_id = int(request.args.get('channel_id'))
    start = int(request.args.get('start'))
    return_dict = channel_messages_v1(token, channel_id, start)
    print(return_dict)
    return dumps(return_dict)

@APP.route("/message/send/v1", methods=["POST"])
def send_message():
    data = request.get_json()

    token = data['token']
    channel_id = data['channel_id']
    message = data['message']

    message_id = message_send(token, channel_id, message)
    return dumps(message_id)

@APP.route("/message/edit/v1", methods=["PUT"])
def edit_message():
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    message = data['message']
    
    message_edit(token, message_id, message)
    return dumps({})

@APP.route("/message/remove/v1", methods=["DELETE"])
def remove_message():
    data = request.get_json()

    token = data['token']
    message_id = int(data['message_id'])
    
    message_remove(token, message_id)   
    return dumps({})

@APP.route("/users/all/v1", methods=["GET"])
def users():
    token = request.args.get('token')

    all_users = users_all_v1(token)
    return dumps(all_users)

@APP.route("/user/profile/v1", methods=["GET"])
def profile_users():
    data = request.get_json()

    token = request.args.get('token')
    u_id = request.args.get('u_id')

    user_profile = user_profile_v1(token, u_id)
    return dumps(user_profile)

@APP.route("/user/profile/setname/v1", methods=["PUT"])
def profile_setname():
    data = request.get_json()

    token = data["token"]
    name_first = data["name_first"]
    name_last = data["name_last"]

    profile_set_name = user_profile_setname_v1(token, name_first, name_last)
    return dumps(profile_set_name)

@APP.route("/user/profile/setemail/v1", methods=["PUT"])
def profile_setemail():
    data = request.get_json()

    token = data["token"]
    email = data["email"]

    profile_set_email = user_profile_setemail_v1(token, email)
    return dumps(profile_set_email)

@APP.route("/user/profile/sethandle/v1", methods=["PUT"])
def sethandle():
    data = request.get_json()

    token = data["token"]
    handle_str = data['handle']

    profile_set_handle = user_profile_sethandle_v1(token, handle_str)
    return dumps(profile_set_handle)

@APP.route("/dm/create/v1", methods=['POST'])
def create_dm():
    data = request.get_json()
    dm_dict = dm_create(data['token'], data['u_ids'])
    return dumps(dm_dict)

@APP.route("/dm/list/v1", methods=['GET'])
def list_dm():
    data = request.args.get('token')
    dm_list_generated = dm_list(data)

    return dumps(dm_list_generated)

@APP.route('/dm/remove/v1', methods=['DELETE'])
def remove_dm():
    data = request.get_json()
    return dumps(dm_remove(data['token'], data['dm_id']))

@APP.route('/dm/details/v1', methods=['GET'])
def details_dm():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    details = dm_details(token, dm_id)
    return dumps(details)        

@APP.route("/dm/leave/v1", methods=['POST'])
def leave_dm():
    data = request.get_json()
    dm_leave(data['token'], data['dm_id'])
    return dumps({})

@APP.route("/dm/messages/v1", methods=['GET'])
def messages_dm():
    token = request.args.get('token')
    dm_id = request.args.get('dm_id')
    start = request.args.get('start')
    messages_dict = dm_messages(token, dm_id, start)
    return dumps(messages_dict)



#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
