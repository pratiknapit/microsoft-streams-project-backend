import pytest
from src.auth import auth_register_v1 
from src.error import InputError, AccessError  
from src.channel import channel_details_v1 
from src.channels import channels_create_v1
from src.other import clear_v1

#Create a dummy user 
steven_dummy = auth_register_v1('stevenchen@gmail.com','workingpassword','steven','chen')
steven = channels_create_v1(steven_dummy['auth_user_id'], 'steven_channel', True)
jacky_dummy = auth_register_v1('jackyzhu@gmail.com','passwordworking','jacky','zhu')
jacky = channels_create_v1(jacky_dummy['auth_user_id'],'jacky_channel',True)

def test_invalid_channel_details():
    clear_v1()
    with pytest.raises(AccessError):
        channel_details_v1(steven_dummy['auth_user_id'], jacky['channel_id'])
    with pytest.raises(InputError):
        channel_details_v1(steven_dummy['auth_user_id'], 543210)

def test_valid_channel_details():
    clear_v1()
    steven_channel_details = channel_details_v1(steven_dummy['auth_user_id'], steven['channel_id'])
    value = False
    if steven_channel_details['name'] == 'steven_channel':
        if steven_channel_details['is_public'] == True:
            for member in steven_channel_details['owner_members']:
                if member == steven_dummy['auth_user_id']:
                    for mem in steven_channel_details['all_members']:
                        if mem == steven_dummy['auth_user_id']:
                            value = True
    else: 
        value = False
    
    assert (value == True)
    