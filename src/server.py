import sys
import signal
from json import dumps
from flask import Flask, request
from src.channel import channel_join_v1, channel_details_v1
from flask_cors import CORS
from src.error import InputError
from src import config
from src.channels import channels_create_v1, channels_list_v1

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




#### NO NEED TO MODIFY BELOW THIS POINT

if __name__ == "__main__":
    signal.signal(signal.SIGINT, quit_gracefully) # For coverage
    APP.run(port=config.port) # Do not edit this port
