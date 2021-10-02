import pytest

from src.error import InputError
from src.auth import auth_register_v1, auth_login_v1
from src.other import clear_v1

def test_auth_register_email_invalid():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1("yuchaocool.com", "password", "yuchao", "zhu")                  # Invalid email- no @
def test_auth_register_duplicate_email_invalid():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1("smartdummy@gmail.com", "password", "yuchao", "zhu")            # Same user email_repeat_check() 
def test_auth_register_password_invalid():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "pie", "yuchao", "zhu")                 # Password less than 6 characters
def test_auth_register_first_min_invalid():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "", "zhu")                  # name_first less than 1 character
def test_auth_register_last_min_invalid():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "yuchao", "")               # name_last less than 1 character
def test_auth_register_first_max_invalid():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "phoenixreborn12345phoenixreborn12345phoenixreborn12345", "xxxshadowlordxxx")           # name_first more than 50 characters
def test_auth_register_last_max_invalid():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "xxxshadowlordxxx", "drownedangeldrownedangeldrownedangeldrownedangeldrownedangel")     # name_last more than 50 characters



def test_auth_login_email_invalid():
    clear_v1()
    with pytest.raises(InputError):
        assert auth_login_v1("where@", "password")                                               # Invalid email



def test_auth_register_user_valid():
    clear_v1()
    valid_user = auth_register_v1("validummy@gmail.com", "password", "smart", "dummy")
    assert(valid_user == {"auth_user_id": valid_user["u_id"]})


dummy = auth_register_v1("smartdummy@gmail.com", "password", "smart", "dummy")
def test_auth_register_test_dummy():
    clear_v1()
    dummy_id = auth_login_v1("smartdummy@gmail.com", "password")
    assert(dummy == dummy_id)