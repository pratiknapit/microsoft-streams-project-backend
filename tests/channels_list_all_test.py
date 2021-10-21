import pytest

from src.error import AccessError
from src.auth import auth_register_v1
from src.channels import channels_listall_v1, channels_create_v1 
from src.other import clear_v1


#Creating Dummy Variables
"""
dummy1 = auth_register_v1("dummyvariable1@gmail.com", "dummy1pw", "dummy1", "variable")
dummy2 = auth_register_v1("dummyvariable2@gmail.com", "dummy2pw", "dummy2", "variable")
dummy1_id = dummy1['auth_user_id']
dummy2_id = dummy2['auth_user_id']
"""

#Testing Errors
def test_user_is_valid(): 
    clear_v1()
    with pytest.raises(AccessError): 
        channels_listall_v1(12342937485)

def test_user_is_valid2(): 
    clear_v1()
    with pytest.raises(AccessError): 
        channels_listall_v1("1345")

def test_user_is_valid3(): 
    clear_v1()
    with pytest.raises(AccessError): 
        channels_listall_v1("&&")

#Testing functionality
def test_channels_list_all_nonmember_user():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_4 = auth_register_v1('dummyuser4@gmail.com', 'passsssworddd', 'Deal', 'DD')

    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True)
    dummy_user_3_channel = channels_create_v1(dummy_user_3['auth_user_id'], 'dummy_user_3_channel', True) 
    
    #Dummy user 4, who is not part of the channel, is calling channels list all. 
    dummy_user_4_channels_list_all = channels_listall_v1(dummy_user_4['auth_user_id'])

    result = 0
    for channel in dummy_user_4_channels_list_all['channels']:
        if channel['channel_id'] == dummy_user_2_channel['channel_id'] and channel['name'] == "dummy_user_2_channel":
            result += 1
        if channel['channel_id'] == dummy_user_3_channel['channel_id'] and channel['name'] == "dummy_user_3_channel":
            result += 1

    assert (result == 2)

def test_channels_list_all_return_type():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')

    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True)
    dummy_user_3_channel = channels_create_v1(dummy_user_3['auth_user_id'], 'dummy_user_3_channel', True) 
    
    #Dummy user 4, who is not part of the channel, is calling channels list all. 
    channels_list_all = channels_listall_v1(dummy_user_2['auth_user_id'])

    assert (channels_list_all == {
        'channels': [
        	{
        		'channel_id': 1,
        		'name': 'dummy_user_2_channel',
        	},
            {
        		'channel_id': 2,
        		'name': 'dummy_user_3_channel',
        	},
        ],
    })


def test_channels_list_all_multiple_by_user_2():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_4 = auth_register_v1('dummyuser4@gmail.com', 'passsssworddd', 'Deal', 'DD')

    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True)
    dummy_user_3_channel = channels_create_v1(dummy_user_3['auth_user_id'], 'dummy_user_3_channel', True) 
    dummy_user_4_channel = channels_create_v1(dummy_user_4['auth_user_id'], 'dummy_user_4_channel', True)

    #Dummy user 2 is calling channel list all.
    dummy_user_2_channels_list_all = channels_listall_v1(dummy_user_2['auth_user_id'])

    result = 0
    for channel in dummy_user_2_channels_list_all['channels']:
        if channel['channel_id'] == dummy_user_2_channel['channel_id'] and channel['name'] == "dummy_user_2_channel":
            result += 1
        if channel['channel_id'] == dummy_user_3_channel['channel_id'] and channel['name'] == "dummy_user_3_channel":
            result += 1
        if channel['channel_id'] == dummy_user_4_channel['channel_id'] and channel['name'] == "dummy_user_4_channel":
            result += 1
    assert (result == 3)

#def test if channels list all works with different other functions in the iteration

def test_channels_list_all_multiple_by_user_3():
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_4 = auth_register_v1('dummyuser4@gmail.com', 'passsssworddd', 'Deal', 'DD')

    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True)
    dummy_user_3_channel = channels_create_v1(dummy_user_3['auth_user_id'], 'dummy_user_3_channel', True) 
    dummy_user_4_channel = channels_create_v1(dummy_user_4['auth_user_id'], 'dummy_user_4_channel', True)

    #Dummy user 2 is calling channel list all.
    dummy_user_3_channels_list_all = channels_listall_v1(dummy_user_3['auth_user_id'])

    result = 0
    for channel in dummy_user_3_channels_list_all['channels']:
        if channel['channel_id'] == dummy_user_2_channel['channel_id'] and channel['name'] == "dummy_user_2_channel":
            result += 1
        if channel['channel_id'] == dummy_user_3_channel['channel_id'] and channel['name'] == "dummy_user_3_channel":
            result += 1
        if channel['channel_id'] == dummy_user_4_channel['channel_id'] and channel['name'] == "dummy_user_4_channel":
            result += 1
    assert (result == 3)

