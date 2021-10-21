import pytest
from src.error import InputError, AccessError
from src.auth import auth_register_v1
from src.user import user_profile_setemail_v1
from src.channels import channels_create_v1
from src.other import clear_v1
from src.user import users_all_v1
from src.data_store import login_token



@pytest.fixture
def dummy_cases():
    clear_v1()
    # 4 dummy users with details
    auth_register_v1("dummy1@gmail.com", "password1", "First", "one")
    auth_register_v1("dummy2@gmail.com", "password2", "Second", "Two")
    auth_register_v1("dummy3@gmail.com", "password3", "Third", "Three")
    auth_register_v1("dummy4@gmail.com", "password4", "Fourth", "Four")



def test_invalid_token(dummy_cases):
    token = 'invalidtoken'
    with pytest.raises(AccessError):
        assert users_all_v1(login_token)


def test_users_all(dummy_cases):
    assert users_all_v1(login_token) == {
        'users': [
            {
                'u_id': dummy_cases['token'],
                'email': 'dummy1@gmail.com',
                'name_first': 'First',
                'name_last': 'One',
                'handle_str': 'FirstOne',
            }, 
            {
                'u_id': dummy_cases['token'],
                'email': 'dummy2@gmail.com',
                'name_first': 'Second',
                'name_last': 'Two',
                'handle_str': 'SecondTwo',
            },
            {
                'u_id': dummy_cases['token'],
                'email': 'dummy3@gmail.com',
                'name_first': 'Third',
                'name_last': 'Three',
                'handle_str': 'ThirdThree',
            },
            {
                'u_id': dummy_cases['token'],
                'email': 'dummy4@gmail.com',
                'name_first': 'Fourth',
                'name_last': 'Four',
                'handle_str': 'FourthFour',
            },
        ]
    }