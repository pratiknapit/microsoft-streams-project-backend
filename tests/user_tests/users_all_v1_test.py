import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.user import user_profile_setemail_v1
from src.other import clear_v1
from src.user import users_all_v1
from src.data_store import login_token



@pytest.fixture
def dummy_cases():
    clear_v1()
    # 2 dummy users with details
    auth_register_v1("dummy1@gmail.com", "password1", "First", "One")
    user2 = auth_register_v1("dummy2@gmail.com", "password2", "Second", "Two")
    token = user2['token']
    return token


def test_users_all(dummy_cases):
    token = dummy_cases
    result = users_all_v1(token)
    assert result == {'users' : 
        [
            {
                'u_id': 1,
                'email': 'dummy1@gmail.com',
                'name_first': 'First',
                'name_last': 'One',
                'handle_str': 'firstone'
            }, 
            {
                'u_id': 2,
                'email': 'dummy2@gmail.com',
                'name_first': 'Second',
                'name_last': 'Two',
                'handle_str': 'secondtwo'
            }
        ]
    }



def test_invalid_token(dummy_cases):
    token = 'invalidtoken'
    with pytest.raises(AccessError):
        assert users_all_v1(token)

