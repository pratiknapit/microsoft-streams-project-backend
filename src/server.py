import sys
import signal
from json import dumps
from flask import Flask, request
from src.channel import channel_join_v1, channel_details_v1
from flask_cors import CORS
from src.error import InputError
from src import config
from src.channels import channels_create_v1, channels_list_v1
from src.data_store import password_check, email_check, email_repeat_check
from src.other import clear_v1
from src.auth import auth_register_v1, auth_login_v1, auth_logout
from src.message import message_send, message_edit, message_remove

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

<<<<<<< HEAD
=======
@APP.route("/clear/v1", methods=["DELETE"])
def clear():
    clear_v1()
    return dumps({})
>>>>>>> master

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

<<<<<<< HEAD

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
    
    return_channel_list = channels_list_v1(token)
    return dumps(return_channel_list)

@APP.route("/channels/details", methods=['GET'])
def channels_details_v2():
    """
    This is a flask wrapper for the channels_details function.  
    """
    
    #no input for channels_list 
    token = request.args.get('token')
    channel_id = request.args.get('channel_id') #might have hto int this
    
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

    channel_join_v1(token, channel_id)

    return dumps({})


"""

@APP.route("message/send/v1", methods=["POST"])
=======
@APP.route("/message/send/v1", methods=["POST"])
>>>>>>> master
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
"""


#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
