import requests
import pytest
from src.config import url
import json

@pytest.fixture
def dummy_user():
    requests.delete(f"{url}/clear/v1") # Clear the data
    requests.post(f"{url}/auth/register/v1", json={
        "email": "dummy1@gmail.com",
        "password": "password1",
        "name_first": "First",
        "name_last": "One",
    })
    user2 = requests.post(f"{url}/auth/register/v1", json={
        "email": "dummy2@gmail.com",
        "password": "password2",
        "name_first": "Second",
        "name_last": "Two",
    })
    payload = user2.json
    return payload


def test_valid_case_setname(dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_first_name = "Jason"
    new_last_name = "Bourne"
    registration = requests.put(f"{url}/user/profile/setname/v1", json={
        'token': user_token,
        'name_first': new_first_name,
        'name_last': new_last_name,
    })
    payload = registration.json()
    assert payload == {}

def test_invalid_short_first_name(dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_first_name = ""
    new_last_name = "Bourne"
    registration = requests.put(f"{url}/user/profile/setname/v1", json={
        'token': user_token,
        'name_first': new_first_name,
        'name_last': new_last_name,
    })
    payload = registration.json()
    assert payload['code'] == 400 # InputError

def test_invalid_long_first_name(dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_first_name = "d"*99
    new_last_name = "Bourne"
    registration = requests.put(f"{url}/user/profile/setname/v1", json={
        'token': user_token,
        'name_first': new_first_name,
        'name_last': new_last_name,
    })
    payload = registration.json()
    assert payload['code'] == 400 # InputError

def test_invalid_short_last_name(dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_first_name = "Jason"
    new_last_name = ""
    registration = requests.put(f"{url}/user/profile/setname/v1", json={
        'token': user_token,
        'name_first': new_first_name,
        'name_last': new_last_name,
    })
    payload = registration.json()
    assert payload['code'] == 400 # InputError

def test_invalid_long_last_name(dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_first_name = "Jason"
    new_last_name = "d"*99
    registration = requests.put(f"{url}/user/profile/setname/v1", json={
        'token': user_token,
        'name_first': new_first_name,
        'name_last': new_last_name,
    })
    payload = registration.json()
    assert payload['code'] == 400 # InputError
