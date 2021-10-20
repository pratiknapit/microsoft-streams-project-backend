import pytest
import jwt
import string
import random
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.message import message_send
from src.error import InputError, AccessError
from src.other import clear_v1
from src.data_store import data_store, is_valid_token

@pytest.fixture
def token():
    clear_v1
    email = "test@unsw.au"
    password = "testPassword"
    firstname = "firstName"
    lastname = "lastName"
    return auth_register_v1(email, password, firstname, lastname)['token']

@pytest.fixture
def channel_id(token):
    return channels_create_v1(token, 'testChannel01', False)['channel_id']

@pytest.fixture
def clear():
    clear_v1()

# Message_send #
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

# Message_edit #
