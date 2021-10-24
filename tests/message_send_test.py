import pytest
import jwt
import string
import random
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.message import message_send
from src.error import InputError, AccessError
from src.other import clear_v1
from src.channel import channel_messages_v1

@pytest.fixture
def token():
    clear_v1
    email = "test@unsw.au"
    password = "testPassword"
    firstname = "firstName"
    lastname = "lastName"
    return auth_register_v1(email ,password, firstname, lastname)['token']

@pytest.fixture
def channel_id(token):
    return channels_create_v1(token, 'testChannel01', False)['channel_id']

@pytest.fixture
def clear():
    clear_v1()

def test_message_too_long(clear, token, channel_id):
    message = ''.join(random.choices(string.ascii_letters, k = 1001))
    with pytest.raises(InputError):
        message_send(token, channel_id, message)

def test_invalid_token(clear, token, channel_id):
    invalid_token = jwt.encode({'test' : 'value'}, 'TestSecret', algorithm='HS256')
    with pytest.raises(AccessError):
        message_send(invalid_token, channel_id, 'testMessage')

def test_user_not_in_channel(clear, token, channel_id):
    second_token = auth_register_v1('test2@unsw.au', 'testPassword', 'secondFirst', 'secondLast')
    with pytest.raises(AccessError):
        message_send(second_token['token'], channel_id, 'testMessage')

def test_message_ids_are_unique(clear, token, channel_id):
    first_id = message_send(token, channel_id, 'testMessaage')['message_id']
    second_id = message_send(token, channel_id, 'secondTestMessage')['message_id']
    assert first_id != second_id

def test_invalid_channel_id(clear, token):
    with pytest.raises(InputError):
        message_send(token, 'channel_id', 'test message')


#############################
#General functionality check#
#############################

def test_message_send():
    '''
    Testing message_send function
    '''
    clear_v1()

    #Creating users to create channels
    user1 = auth_register_v1("user1@gmail.com", "user1pass", "user1", "last1")
    user2 = auth_register_v1("user2@gmail.com", "user2pass", "user2", "last2")
    token1 = user1['token']
    token2 = user2['token']

    #creating channels
    ch_id1 = channels_create_v1(token1, "aGreatChannel", True)['channel_id']
    ch_id2 = channels_create_v1(token2, "yetAnotherChannel", False)['channel_id']

    #error test
    with pytest.raises(InputError):
        #message too long
        message_send(token1, ch_id1, 'h'*1001)

    with pytest.raises(AccessError):
        #user not in channel
        message_send(token1, ch_id2, "ilegal")

    #creating channel messages
    message_send(token1, ch_id1, 'h'*1000)
    message_send(token1, ch_id1, 'hey')

    message_send(token2, ch_id2, "hello")
    message_send(token2, ch_id2, "hello")
    message_send(token2, ch_id2, "hello")

    #checking messages have been added
    print(channel_messages_v1(token1, ch_id1, 0))
    assert len(channel_messages_v1(token1, ch_id1, 0)['messages']) == 2
    assert len(channel_messages_v1(token2, ch_id2, 0)['messages']) == 3