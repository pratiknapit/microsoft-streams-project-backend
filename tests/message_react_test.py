import re
import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1, channels_list_v1
from src.channel import channel_join_v1, channel_leave_v2, channel_add_owner_v2, channel_details_v1, channel_remove_owner_v2
from src.data_store import channel_id_check, data_store, message_id_check
from src.message import message_react_v1, message_send, message_edit, message_remove, message_share_v1, message_unreact_v1
from src.other import clear_v1
from src.dm import dm_create 

@pytest.fixture
def clear():
    clear_v1()

@pytest.fixture
def user1():
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    return dummy_user_1

@pytest.fixture
def channel1(user1):
    channel_user1 = channels_create_v1(user1['token'], "channel1", True)
    return channel_user1

@pytest.fixture
def channel2(user1):
    channelpriv_user1 = channels_create_v1(user1['token'], "channelPriv", False)
    return channelpriv_user1

@pytest.fixture
def user2():
    dummy_user_2 = auth_register_v1('dummy2my@gmail.com', 'random', 'Jack', 'Grealish')
    return dummy_user_2

@pytest.fixture
def user3():
    dummy_user_3 = auth_register_v1('dummy333my@gmail.com', 'yessiaf', 'Pra', 'Beckham')
    return dummy_user_3


def test_react_channel(clear, user1, user2, channel1): 
    message = "hello"
    message_id = message_send(user1['token'], channel1['channel_id'], message)['message_id']
    channel = channel_id_check(channel1['channel_id'])
    for msg in channel['Messages']:
        if msg['message_id'] == message_id:
            assert message == msg['message']
    
    channel_join_v1(user2['token'], channel1['channel_id'])

    assert {} == message_react_v1(user2['token'], message_id, 1)

    message = message_id_check(message_id)

    assert message['reacts'][0]['u_ids'] == [user2['auth_user_id']]

def test_unreact_channel(clear, user1, user2, channel1): 
    message = "hello"
    message_id = message_send(user1['token'], channel1['channel_id'], message)['message_id']
    channel = channel_id_check(channel1['channel_id'])
    for msg in channel['Messages']:
        if msg['message_id'] == message_id:
            assert message == msg['message']
    
    channel_join_v1(user2['token'], channel1['channel_id'])

    assert {} == message_react_v1(user2['token'], message_id, 1)

    message = message_id_check(message_id)

    assert message['reacts'][0]['u_ids'] == [user2['auth_user_id']]

    assert {} == message_unreact_v1(user2['token'], message_id, 1)

    message = message_id_check(message_id)

    assert message['reacts'][0]['u_ids'] != [user2['auth_user_id']]
    assert message['reacts'][0]['u_ids'] == []


