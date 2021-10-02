import pytest
from src.auth import auth_register_v1 
from src.error import InputError, AccessError  
from src.channel import channel_details_v1 
from src.channels import channels_create_v1, channels_list_v1
from src.other import clear_v1

'''
#Create a dummy user 
steven_dummy = auth_register_v1('stevenchen@gmail.com','workingpassword','steven','chen')
steven = channels_create_v1(steven_dummy['auth_user_id'], 'steven_channel', True)
jacky_dummy = auth_register_v1('jackyzhu@gmail.com','passwordworking','jacky','zhu')
jacky = channels_create_v1(jacky_dummy['auth_user_id'],'jacky_channel',True)
'''

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

    with pytest.raises(AccessError):
        channel_details_v1(dummy_user_3['auth_user_id'], dummy_user_2_channel['channel_id'])
    with pytest.raises(InputError):
        channel_details_v1(dummy_user_2['auth_user_id'], 63043)

def test_valid_channel_details(clear):
    clear_v1()
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')
    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True)
    dummy_user_2_list_channel = channels_list_v1(dummy_user_2['auth_user_id'])

    dummy_user_2_list = dummy_user_2_list_channel['channels'][0]
    
    value = False
    if dummy_user_2_list['name'] == 'dummy_user_2_channel':
        # if dummy_user_2_channel['is_public'] == True:
        # for member in dummy_user_2_channel['owner_members']:
        for mem in dummy_user_2_list['all_members']:
            if mem == dummy_user_2['auth_user_id']:
                value = True
    else: 
        value = False
    
    assert (value == True)
    