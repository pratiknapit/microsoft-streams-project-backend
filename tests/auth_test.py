import re
import pytest

from src.error import InputError
from src.auth import auth_register_v1


regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


#def test_check(email):
#		if (re.fullmatch(regex, email)) == None:            # If email is invalid
#			with pytest.raises(InputError)
#                assert auth_register_v1("yuchaocool.com", "", "", "")




def test_auth_register_email_invalid():
    with pytest.raises(InputError):
        assert auth_register_v1("yuchaocool.com", "password", "yuchao", "zhu")                  # Invalid email- no @
#        assert auth_register_v1("yuchaocool@", "password", "yuchao", "zhu")                    # Same user      
def test_auth_register_password_invalid():
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "pie", "yuchao", "zhu")                 # Password less than 6 characters
def test_auth_register_first_min_invalid():
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "", "zhu")                  # name_first less than 1 character
def test_auth_register_last_min_invalid():
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "yuchao", "")               # name_last less than 1 character
def test_auth_register_first_max_invalid():
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "phoenixreborn12345phoenixreborn12345phoenixreborn12345", "xxxshadowlordxxx")           # name_first more than 50 characters
def test_auth_register_last_max_invalid():
    with pytest.raises(InputError):
        assert auth_register_v1("jackysydau@gmail.com", "password", "xxxshadowlordxxx", "drownedangeldrownedangeldrownedangeldrownedangeldrownedangel")     # name_last more than 50 characters

