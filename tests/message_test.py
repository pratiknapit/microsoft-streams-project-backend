import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.channels import channels_create_v1
#from src.channel import channel_messages_v1
from src.message import message_send
from src.other import clear_v1


@pytest.fixture
def dummy_cases():
    # Dummy case created for testing of different parts of channel_invite_v1
    dummy_user_1 = auth_register_v1('dummyuser1@gmail.com', 'passworddd', 'Alpha', 'AA')
    dummy_user_2 = auth_register_v1('dummyuser2@gmail.com', 'yessword', 'Beta', 'BB')
    dummy_user_3 = auth_register_v1('dummyuser3@gmail.com', 'passsssword', 'Ceal', 'CC')

    # Creating a new channel with the first member as an owner and member
    dummy_user_2_channel = channels_create_v1(dummy_user_2['auth_user_id'], 'dummy_user_2_channel', True) # true means public channel
    dummy_user_2_message = message_send(dummy_user_2['token'], dummy_user_2['channel_id'], "Dummys message")

    combined_data = {
        "dummy_user_1": dummy_user_1,
        "dummy_user_2": dummy_user_2,
        "dummy_user_3": dummy_user_3,
        "dummy_user_2_channel": dummy_user_2_channel,
        "dummy_user_2_message": dummy_user_2_message,
    }
    return combined_data

@pytest.fixture
def clear():
    clear_v1()


#def test_message_send_invalid_InputError(clear, dummy_cases):
    with pytest.raises(InputError):
        message_send(dummy_cases['dummy_user_2']['token'], dummy_cases['dummy_user_2_channel']['channel_id'], "H"*1001)







