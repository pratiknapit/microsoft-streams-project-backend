import pytest

from src.error import AccessError
from src.auth import auth_register_v1
from src.channels import channels_listall_v1, channels_create_v1, channels_list_v1
from src.channel import channel_invite_v1, channel_join_v1
from src.other import clear_v1

def test_invalid_token():
    clear_v1()
    with pytest.raises(AccessError): 
        channels_list_v1("random_token")

def test_invalid_token2():
    clear_v1()
    with pytest.raises(AccessError): 
        channels_listall_v1("random_token")

def test_user_is_invalid(): 
    clear_v1()
    with pytest.raises(AccessError): 
        channels_listall_v1(12342384735)

def test_user_is_invalid2(): 
    clear_v1()
    with pytest.raises(AccessError): 
        channels_listall_v1("1345")

def test_user_is_invalid3(): 
    clear_v1()
    with pytest.raises(AccessError): 
        channels_listall_v1("&&")

def test_channels_list_non_member():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_4 = auth_register_v1('dummyuser4@gmail.com', 'passsssworddd', 'Deal', 'DD')

    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True)
    dummy_user_3_channel = channels_create_v1(dummy_user_3['token'], 'dummy_user_3_channel', True) 
    
    #Dummy user 4, who is not part of the channel, is calling channels list all. 
    dummy_user_4_channels_list = channels_list_v1(dummy_user_4['token'])['channels']

    result = 0
    for channel in dummy_user_4_channels_list:
        if channel['channel_id'] == dummy_user_2_channel['channel_id'] and channel['name'] == "dummy_user_2_channel":
            result += 1
        if channel['channel_id'] == dummy_user_3_channel['channel_id'] and channel['name'] == "dummy_user_3_channel":
            result += 1

    assert (result == 0)

def test_channels_list_member():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    
    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True)
    dummy_user_3_channel = channels_create_v1(dummy_user_3['token'], 'dummy_user_3_channel', True) 
    
    #Dummy user 4, who is not part of the channel, is calling channels list all. 
    dummy_user_2_channels_list = channels_list_v1(dummy_user_2['token'])['channels']

    result = 0
    for channel in dummy_user_2_channels_list:
        if channel['channel_id'] == dummy_user_2_channel['channel_id'] and channel['name'] == "dummy_user_2_channel":
            result += 1
        if channel['channel_id'] == dummy_user_3_channel['channel_id'] and channel['name'] == "dummy_user_3_channel":
            result += 1

    assert (result == 1)


def test_channels_list_member_and_join_member():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_4 = auth_register_v1('dummyuser4@gmail.com', 'passsssworddd', 'Deal', 'DD')

    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True)
    dummy_user_3_channel = channels_create_v1(dummy_user_3['token'], 'dummy_user_3_channel', True) 
    
    channel_join_v1(dummy_user_4['token'], dummy_user_2_channel['channel_id'])

    #Dummy user 4, who is not part of the channel, is calling channels list all. 
    dummy_user_4_channels_list = channels_list_v1(dummy_user_4['token'])['channels']

    result = 0
    for channel in dummy_user_4_channels_list:
        if channel['channel_id'] == dummy_user_2_channel['channel_id'] and channel['name'] == "dummy_user_2_channel":
            result += 1
        if channel['channel_id'] == dummy_user_3_channel['channel_id'] and channel['name'] == "dummy_user_3_channel":
            result += 1

    assert (result == 1)

def test_channels_list_member_and_join_member2():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_4 = auth_register_v1('dummyuser4@gmail.com', 'passsssworddd', 'Deal', 'DD')

    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True)
    dummy_user_3_channel = channels_create_v1(dummy_user_3['token'], 'dummy_user_3_channel', True) 
    
    channel_join_v1(dummy_user_4['token'], dummy_user_2_channel['channel_id'])
    channel_join_v1(dummy_user_4['token'], dummy_user_3_channel['channel_id'])
    
    #Dummy user 4, who is not part of the channel, is calling channels list all. 
    dummy_user_4_channels_list = channels_list_v1(dummy_user_4['token'])['channels']

    result = 0
    for channel in dummy_user_4_channels_list:
        if channel['channel_id'] == dummy_user_2_channel['channel_id'] and channel['name'] == "dummy_user_2_channel":
            result += 1
        if channel['channel_id'] == dummy_user_3_channel['channel_id'] and channel['name'] == "dummy_user_3_channel":
            result += 1

    assert (result == 2)


def test_channels_list_member_and_invite_member():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')

    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True)
    
    #empty_dict3 = channel_invite_v1(dummy_user_2['auth_user_id'], dummy_user_2_channel['channel_id'], dummy_user_3['auth_user_id'])

    #Dummy user 2, who is part of the channel, is calling channels list. 
    dummy_user_2_channels_list = channels_list_v1(dummy_user_2['token'])['channels']

    result = 0
    for channel in dummy_user_2_channels_list:
        if channel['channel_id'] == dummy_user_2_channel['channel_id'] and channel['name'] == "dummy_user_2_channel":
            result += 1

    assert (result == 1)


def test_channels_list_member_and_invite_member2():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')

    dummy_user_2_channel = channels_create_v1(dummy_user_2['token'], 'dummy_user_2_channel', True)
    dummy_user_3_channel = channels_create_v1(dummy_user_3['token'], 'dummy_user_3_channel', True)

    channel_invite_v1(dummy_user_2['token'], dummy_user_2_channel['channel_id'], dummy_user_3['auth_user_id'])

    #Dummy user 3, who is not part of the channel, is calling channels list. 
    dummy_user_3_channels_list = channels_list_v1(dummy_user_3['token'])['channels']

    result = 0
    for channel in dummy_user_3_channels_list:
        if channel['channel_id'] == dummy_user_2_channel['channel_id'] and channel['name'] == "dummy_user_2_channel":
            result += 1
        if channel['channel_id'] == dummy_user_3_channel['channel_id'] and channel['name'] == "dummy_user_3_channel":
            result += 1

    assert (result == 2)
