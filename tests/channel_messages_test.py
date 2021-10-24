import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1
from src.channel import channel_messages_v1
from src.message import message_send
from src.other import clear_v1
from src.data_store import data_store

#################
#Version 1 Tests#
#################

#creating clear and dummy cases fixtures to use in every test
@pytest.fixture
def dummy_cases():
    # Dummy case created for testing of different parts of channel_invite_v1
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')

    # Creating a new channel with the first member as an owner and member
    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True) # true means public channel
    combined_data = {
        "dummy_user_1": dummy_user_1,
        "dummy_user_2": dummy_user_2,
        "dummy_user_3": dummy_user_3,
        "dummy_user_2_channel": dummy_user_2_channel,
    }
    return combined_data

@pytest.fixture
def clear():
    clear_v1()

def test_channel_messages_channel_id_invalid(clear, dummy_cases):
    # Channel id is incorrect (no such channel id exists)
    with pytest.raises(InputError):
        channel_messages_v1(dummy_cases['dummy_user_2']['token'], 23455, 39283)

def test_channel_messages_start_greater_than_total_messages_error(clear, dummy_cases):
    # Total messages is less than start (causes error)
    with pytest.raises(InputError):
        channel_messages_v1(dummy_cases['dummy_user_2']['token'],
        dummy_cases['dummy_user_2_channel']['channel_id'], 34)

def test_channel_messages_auth_not_in_channel_invalid(clear, dummy_cases):
    # Correct auth_user_id but they are not a member of the channel
    with pytest.raises(AccessError):
        channel_messages_v1(dummy_cases['dummy_user_1']['token'],
        dummy_cases['dummy_user_2_channel']['channel_id'], 234)

def test_channel_messages_functionality(clear, dummy_cases):
    assert channel_messages_v1(dummy_cases['dummy_user_2']['token'],
    dummy_cases['dummy_user_2_channel']['channel_id'], 0) == {
        'messages': [],
        'start': 0,
        'end':-1 
    }

#################
#Version 2 Tests#
#################

@pytest.fixture
def token():
    # create a test user and return auth_id
    email = "testmail@gamil.com"
    password = "Testpass12345"
    token = auth_register_v1(email, password, "firstname", "lastname")['token']
    return token

@pytest.fixture
def channel_id(token):
    # create a public channel and return channel_id
    return channels_create_v1(token, "channelName1", True)['channel_id']

@pytest.fixture
def unauthorised_user():
    email = "testmail2@gamil.com"
    password = "Testpass1234567"
    token = auth_register_v1(email, password, "firstname", "lastname")['token']
    return token

def test_invalid_token(clear, channel_id):
    with pytest.raises(AccessError):
        channel_messages_v1("invalid_token", channel_id, 0)
    clear_v1()

def test_invalid_channel_id(clear, token, channel_id):
    with pytest.raises(InputError):
        channel_messages_v1(token, channel_id + 1, 0)
    clear_v1()

def test_user_not_in_channel(clear, unauthorised_user, channel_id):
    # Test an user that does not belong to the channel with the given channel_id
    with pytest.raises(AccessError):
        channel_messages_v1(unauthorised_user, channel_id, 0)
    clear_v1()

def test_invalid_start(clear, token, channel_id):
    # this fail because no message is being sent to the channel yet
    with pytest.raises(InputError):
        channel_messages_v1(token, channel_id, 51)
    clear_v1()

def test_last_message(clear, token, channel_id):
    # Test if end = -1 when there are no more messages to load after the current return
    message_send(token, channel_id, "Hi, everyone!")
    end = channel_messages_v1(token, channel_id, 0)['end']
    assert end == -1
    clear_v1()