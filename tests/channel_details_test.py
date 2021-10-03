import pytest
from src.auth import auth_register_v1 
from src.error import InputError, AccessError  
from src.channel import channel_details_v1 
from src.channels import channels_create_v1, channels_list_v1
from src.other import clear_v1

@pytest.fixture
def dummy_cases():
    # Dummy case created for testing of different parts of channel_invite_v1
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    # Creating a new channel with the first member as an owner and member
    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True) # true means public channel
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

def test_invalid_channel_details(clear):
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True)

def test_valid_channel_details(clear):
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True)
    dummy_user_2_list_channel = channels_list_v1(dummy_user_2['auth_user_id'])

    dummy_user_2_list = dummy_user_2_list_channel['channels'][0]
    
    channel = channel_details_v1(dummy_user_2['auth_user_id'], dummy_user_2_channel['channel_id'])

    value = False
    if channel['name'] == 'dummy_user_2_channel':
        if channel['is_public'] == True:
            for member in channel['owner_members']:
                if member['u_id'] == dummy_user_2['auth_user_id']:
                    for mem in channel['all_members']:
                        if mem['u_id'] == dummy_user_2['auth_user_id']:
                            value = True 
    else: 
        value = False
    
    assert (value == True)
    