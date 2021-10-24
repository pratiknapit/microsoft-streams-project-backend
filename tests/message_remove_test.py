import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.dm import dm_create, dm_messages
from src.channels import channels_create_v1
from src.channel import channel_join_v1, channel_messages_v1
from src.message import message_send, message_remove
from src.error import InputError, AccessError


@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def auth_user():
    email = "testmail@gamil.com"
    password = "Testpass12345"
    auth_user_info = auth_register_v1(email, password, "firstname", "lastname")
    token = auth_user_info['token']
    return token

@pytest.fixture
def member():
    email = "testmail1@gamil.com"
    password = "Testpass123456"
    first_name = "firstone"
    last_name = "lastone"
    member = auth_register_v1(email, password, first_name, last_name)
    return member

@pytest.fixture
def channel_id(auth_user, member):
    channel_id = channels_create_v1(auth_user, "channelName", True)['channel_id']
    channel_join_v1(member['token'], channel_id)
    return channel_id

@pytest.fixture
def dm_id(auth_user, member):
    dm_id = dm_create(auth_user, [member['auth_user_id']])['dm_id']
    return dm_id

def test_remove_channel_message(clear, auth_user, channel_id):
    message_id = message_send(auth_user, channel_id, "Hi!")['message_id']
    channel_messages_count_before = len(channel_messages_v1(auth_user, channel_id, 0)['messages'])
    assert channel_messages_count_before == 1

    message_remove(auth_user, message_id)
    assert len(channel_messages_v1(auth_user, channel_id, 0)['messages']) == 0

def test_invalid_token(clear, auth_user, channel_id):
    channel_message_id = message_send(auth_user, channel_id, "Hi!")['message_id']
    with pytest.raises(AccessError):
        message_remove("invalid_token", channel_message_id)

def test_unauthorised_auth_user(clear, auth_user, member, channel_id):
    channel_message_id = message_send(auth_user, channel_id, "Hi!")['message_id']
    with pytest.raises(AccessError):
        message_remove(member['token'], channel_message_id)

def test_invalid_message_id(clear, auth_user):
    with pytest.raises(InputError):
        message_remove(auth_user, 1)

def test_dm_message_count(clear, auth_user, dm_id):
    dm_message_count = len(dm_messages(auth_user, dm_id, 0)['messages'])
    assert dm_message_count == 0