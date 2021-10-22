
import pytest
import jwt
import string
import random
from src.auth import auth_register_v1
from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.message import message_send, message_edit
from src.dm import dm_create, dm_messages
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
@pytest.fixture(autouse=True)
def clear():
    clear_v1()
    yield
    clear_v1()


@pytest.fixture
def admin():
    return auth_register_v1('test@unsw.au', 'password1', 'first1', 'last1')

@pytest.fixture
def member():
    return auth_register_v1('test1@unsw.au', 'password2', 'first2', 'last2')

@pytest.fixture
def channel(admin):
    return channels_create_v1(admin['token'], 'channel_1', True)

@pytest.fixture
def dm(admin, member):
    return dm_create(admin['token'], [member['auth_user_id']])

@pytest.fixture
def channel_message(admin, channel):
    return message_send(admin['token'], channel['channel_id'], 'this is a message sent to the other user in the channel.')
'''
@pytest.fixture
def dm_message(admin, dm):
    return message_senddm_v1(admin['token'], dm['dm_id'], 'this is a message sent to the other user.')
'''
'''
def test_invalid_token_dm(dm_message):
    invalid_token = 'invalidtoken123123'
    with pytest.raises(AccessError):
        message_edit(
            invalid_token, dm_message['message_id'], 'this is an updated message in the dm.')
'''


def test_invalid_token_channel(channel_message):
    invalid_token = 'invalidtoken123123'
    with pytest.raises(AccessError):
        message_edit(
            invalid_token, channel_message['message_id'], 'this is an updated message in the dm.')

'''
def test_message_incorrect_length_dm(admin, dm_message):
    with pytest.raises(InputError):
        message_edit(admin['token'], dm_message['message_id'], 1500*'A')
'''


def test_message_incorrect_length_channel(admin, channel_message):
    with pytest.raises(InputError):
        message_edit(
            admin['token'], channel_message, 1500*'A')


def test_message_sent_by_unauthorised_user_and_not_channel_owner(admin, member, channel_message):
    with pytest.raises(AccessError):
        message_edit(member['token'], channel_message['message_id'],
                        'this is an updated message in the dm.')


def test_success_channel_message(admin, channel, channel_message):
    message_edit(admin['token'], channel_message['message_id'],
                    'this edit is valid in this channel.')
    channel_messages = channel_messages_v1(
        admin['token'], channel['channel_id'], 0)
    assert channel_messages['message'] == 'this edit is valid in this channel.'

'''    
def test_success_dm_message(admin, dm, dm_message):
    message_edit(admin['token'], dm_message['message_id'],
                    'this edit is valid in this dm.')
    dm_messaging = dm_messages(admin['token'], dm['dm_id'], 0)
    assert dm_messaging['messages'][0]['message'] == 'this edit is valid in this dm.'  
'''  