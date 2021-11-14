import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.user import user_profile_setemail_v1
from src.other import clear_v1
from src.user import users_all_v1
from src.data_store import login_token
from src.user import user_stats_v1

@pytest.fixture
def dummy_cases():
    clear_v1()
    # 2 dummy users with details
    user1 = auth_register_v1("dummy1@gmail.com", "password1", "First", "One")
    token = user1['token']
    return token

'''
def test_invalid_token(dummy_cases):
    token = 'pleasegiveushighermarks'
    with pytest.raises(AccessError):
        assert user_stats_v1(token)

def test_valid_case(dummy_cases):
    token = dummy_cases
    result = user_stats_v1(token)
    assert res['channels_joined'][-1]['num_channels_joined'] == 0
    assert res['dms_joined'][-1]['num_dms_joined'] == 0
    assert res['messages_sent'][-1]['num_messages_sent'] == 0
    assert res['involvement_rate'] == 0

'''
def test_channels_stats(dummy_cases):
    pass

def test_dm_stats(dummy_cases):
    pass

def test_messages_stats(dummy_cases):
    pass    
