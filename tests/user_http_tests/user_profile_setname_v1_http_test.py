import requests
import pytest
from src import config
import json

@pytest.fixture
def dummy_user():
    requests.post(config.url + "/auth/register/v2", json={
        "email": "dummy1@gmail.com",
        "password": "password1",
        "name_first": "First",
        "name_last": "One",
    })
    user2 = requests.post(config.url + "/auth/register/v2", json={
        "email": "dummy2@gmail.com",
        "password": "password2",
        "name_first": "Second",
        "name_last": "Two",
    })
    payload = user2.json()
    return payload

@pytest.fixture
def clear():
    requests.delete(config.url + "/clear/v1")

def test_valid_case_setname(clear, dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_first_name = "Yes"
    new_last_name = "Yeetus"
    result = requests.put(config.url + "/user/profile/setname/v1", json={
        'token': user_token,
        'name_first': new_first_name,
        'name_last': new_last_name,
    })
    payload = result.json()
    assert payload == {}

def test_invalid_short_first_name(clear, dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_first_name = ""
    new_last_name = "Yeetus"
    result = requests.put(config.url + "/user/profile/setname/v1", json={
        'token': user_token,
        'name_first': new_first_name,
        'name_last': new_last_name,
    })
    payload = result.json()
    assert payload['code'] == 400 # InputError

def test_invalid_long_first_name(clear, dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_first_name = "d"*99
    new_last_name = "Yeetus"
    result = requests.put(config.url + "/user/profile/setname/v1", json={
        'token': user_token,
        'name_first': new_first_name,
        'name_last': new_last_name,
    })
    payload = result.json()
    assert payload['code'] == 400 # InputError

def test_invalid_short_last_name(clear, dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_first_name = "Yes"
    new_last_name = ""
    result = requests.put(config.url + "/user/profile/setname/v1", json={
        'token': user_token,
        'name_first': new_first_name,
        'name_last': new_last_name,
    })
    payload = result.json()
    assert payload['code'] == 400 # InputError

def test_invalid_long_last_name(clear, dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_first_name = "Yes"
    new_last_name = "d"*99
    result = requests.put(config.url + "/user/profile/setname/v1", json={
        'token': user_token,
        'name_first': new_first_name,
        'name_last': new_last_name,
    })
    payload = result.json()
    assert payload['code'] == 400 # InputError
