from src.message import message_pin, message_send, message_senddm
import pytest
from src.other import clear_v1
from src.auth import auth_register_v1
from src.channel import channel_messages_v1
from src.channels import channels_create_v1
from src.dm import dm_create, dm_messages
from src.error import InputError, AccessError


@pytest.fixture(autouse=True)
def clear():
    clear_v1()
    yield
    clear_v1()


@pytest.fixture
def admin():
    owner = auth_register_v1(
        'test@gmail.com', 'password', 'firstname', 'lastname')
    return owner


@pytest.fixture
def member():
    member = auth_register_v1('testmember@gmail.com',
                              'password1', 'memberfirst', 'memberlast')
    return member


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
def dm_message(admin, dm):
    return message_senddm(admin['token'], dm['dm_id'], 'this is a message sent to the other user.')


@pytest.fixture
def not_member():
    return auth_register_v1(
        'notmember@unsw.au', 'password123', 'notmemberfirst', 'notmemberlast')


def test_invalid_message_id(admin, channel):
    with pytest.raises(InputError):
        message_pin(admin['token'], 123)


def test_message_already_pinned_channel(admin, channel, channel_message):
    message_pin(admin['token'], channel_message['message_id'])
    with pytest.raises(InputError):
        message_pin(admin['token'], channel_message['message_id'])


def test_message_already_pinned_dm(admin, dm_message):
    message_pin(admin['token'], dm_message['message_id'])
    with pytest.raises(InputError):
        message_pin(admin['token'], dm_message['message_id'])


def test_user_not_member_channel(channel_message, admin, not_member):
    with pytest.raises(AccessError):
        message_pin(not_member['token'], channel_message['message_id'])


def test_user_not_member_dm(dm_message, admin, not_member):
    with pytest.raises(AccessError):
        message_pin(not_member['token'], dm_message['message_id'])


def test_not_channel_owner(admin, member, channel_message):
    with pytest.raises(AccessError):
        message_pin(member['token'], channel_message['message_id'])


def test_not_dm_owner(admin, member, dm_message):
    with pytest.raises(AccessError):
        message_pin(member['token'], dm_message['message_id'])


def test_success_case_channel(admin, member, channel, channel_message):
    message_pin(admin['token'], channel_message['message_id'])
    channel_message_dict = channel_messages_v1(
        admin['token'], channel['channel_id'], 0)
    assert channel_message_dict['messages'][0]['is_pinned'] == True


def test_success_case_dm(admin, member, dm, dm_message):
    message_pin(admin['token'], dm_message['message_id'])
    dm_message_dict = dm_messages(
        admin['token'], dm['dm_id'], 0)
    assert dm_message_dict['messages'][0]['is_pinned'] == True