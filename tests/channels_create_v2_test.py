from flask.wrappers import Response
import pytest
import requests
import json
from src import config

@pytest.fixture
def user1():
    user1 = requests.post(config.url + "auth/register/v2", json={
        "email": "pratik7@gmail.com",
        "password": "ronaldo",
        "name_first": "Pratik",
        "name_last": "Napit"
        })
    return user1.json()

@pytest.fixture
def channel1(user1):
    channel = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "FirstChannel",
        "is_public": True
        })
    return channel.json()

@pytest.fixture
def clear():
    requests.delete(config.url + 'clear/v1')

def test_invalid_token(clear):
    response = requests.post(config.url + 'channels/create/v2', json={
        "token": "random_token",
        "name": "FirstChannel",
        "is_public": True
        })
    assert response.status_code == 403

def test_invalid_name_length1(clear, user1):
    response = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "FirstChanneladfadkfjlkdsjfksdljfakdfajafdksjl",
        "is_public": True
        })
    assert response.status_code == 400

def test_invalid_name_length2(clear, user1):
    response = requests.post(config.url + 'channels/create/v2', json={
        "token": user1['token'],
        "name": "",
        "is_public": True
        })
    assert response.status_code == 400

def test_channel_create_v2_basic(): 
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + "auth/register/v2", json={
        "email": "use4r@gmail.com",
        "password": "dummypass",
        "name_first": "jacky",
        "name_last": "zhu"
        })

    user_payload = response.json()
    assert response.status_code == 200

    response1 = requests.post(config.url + "channels/create/v2", json={
        "token": user_payload['token'],
        "name": "FirstChannel",
        "is_public": "True"
        })

    channel_payload = response1.json()
    assert response1.status_code == 200
    assert channel_payload == {"channel_id": 1}



    
