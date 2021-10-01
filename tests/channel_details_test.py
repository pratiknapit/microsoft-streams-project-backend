import pytest
from src.auth import auth_register_v1 
from src.error import InputError, AccessError  
from src.channel import channel_details_v1 
from src.channels import channels_create_v1

#Create a dummy user 
steven_dummy = auth_register_v1('stevenchen@gmail.com','workingpassword','steven','chen')
steven = channels_create_v1(steven_dummy['auth_user_id'], 'steven_channel', True)
jacky_dummy = auth_register_v1('jackyzhu@gmail.com','passwordworking','jacky','zhu')
jacky = channels_create_v1(jacky_dummy['auth_user_id'],'jacky_channel',True)

def test_invalid_channel_details():
    with pytest.raises(AccessError):
        channel_details_v1(steven_dummy['auth_user_id'], jacky['channel_id'])
    with pytest.raises(InputError):
        channel_details_v1(steven_dummy['auth_user_id'], 543210)

def test_valid_channel_details():
    assert(channel_details(steven_dummy['auth_user_id'], steven_dummy['channel_id']) ==
    {
        'name': 'steven_channel',

        'owner_members': [{'name_first': steven_dummy['name_first'],
        'name_last': steven_dummy['name_last'], 'u_id': steven_dummy['u_id']}],

        'all_members': [{'name_first': steven_dummy['name_first'],
        'name_last': steven_dummy['name_last'], 'u_id': steven_dummy['u_id']}],
    }
    )