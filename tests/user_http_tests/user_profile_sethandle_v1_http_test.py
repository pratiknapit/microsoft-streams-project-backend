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

def test_valid_sethandle(clear, dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_user_handle = "bobmonk"
    result = requests.put(config.url + "/user/profile/sethandle/v1", json={
        'token': user_token,
        'handle_str': new_user_handle,
    })
    payload = result.json()
    assert payload == {}

def test_invalid_handle(clear, dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_user_handle = "bobmonk"*10 # invalid string length
    result = requests.put(config.url + "/user/profile/sethandle/v1", json={
        'token': user_token,
        'handle_str': new_user_handle,
    })
    payload = result.json()
    assert payload['code'] == 400 #InputError

def test_taken_handle(clear, dummy_user):
    user2 = dummy_user
    user_token = user2['token']
    new_user_handle = "firstone" # handle is taken by another user
    result = requests.put(config.url + "/user/profile/sethandle/v1", json={
        'token': user_token,
        'handle_str': new_user_handle,
    })
    payload = result.json()
    assert payload['code'] == 400 #InputError

def test_invalid_token_handle(clear):
    user_token = "nevergonnagiveyouupnevergonnaletyoudown"
    new_user_handle = "bobmonk"
    result = requests.put(config.url + "/user/profile/sethandle/v1", json={
        'token': user_token,
        'handle_str': new_user_handle,
    })
    payload = result.json()
    assert payload ['code'] == 403