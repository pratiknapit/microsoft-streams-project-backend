import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.error import AccessError, InputError
from src.message import message_edit
from src.channels import channels_create_v1
from src.dm import dm_create, dm_messages
from src.message import message_send, message_senddm
from src.channel import channel_messages_v1


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

@pytest.fixture
def dm_msg(admin, dm):
    return message_senddm(admin['token'], dm['dm_id'], 'this is a message sent to the other user.')
'''
def test_invalid_token_dm(dm_msg):
    invalid_token = 'invalidtoken123123'
    with pytest.raises(AccessError):
        message_edit(
            invalid_token, dm_msg['message_id'], 'this is an updated message in the dm.')
'''
def test_invalid_token_channel(channel_message):
    invalid_token = 'invalidtoken123123'
    with pytest.raises(AccessError):
        message_edit(
            invalid_token, channel_message['message_id'], 'this is an updated message in the dm.')

def test_message_incorrect_length_dm(admin, dm_msg):
    with pytest.raises(InputError):
        message_edit(admin['token'], dm_msg['message_id'], 1500*'A')

def test_invalid_msg_id(admin, ):
    with pytest.raises(InputError):
        message_edit(admin['token'], '12673476', 'updated message in dm')

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
    assert channel_messages['messages'][0]['message'] == 'this edit is valid in this channel.'
'''
def test_success_dm_message(admin, dm, dm_msg):
    message_edit(admin['token'], dm_msg['message_id'],
                    'this edit is valid in this dm.')
    dm_mess = dm_messages(admin['token'], dm['dm_id'], 0)
    assert dm_mess['messages'][0]['message'] == 'this edit is valid in this dm.'
'''