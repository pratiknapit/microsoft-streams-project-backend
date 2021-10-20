import pytest
import requests
import json
from src import config

def test_channel_details_v2():
    requests.delete(config.url + 'clear/v1')
    response = requests.post(config.url + "auth/register/v2", json={
        "email": "pratik7@gmail.com",
        "password": "ronaldo",
        "name_first": "Pratik",
        "name_last": "Napit"
        })
    user1_payload = response.json()
    assert response.status_code == 200

    response2 = requests.post(config.url + "auth/register/v2", json={
        "email": "dummy7@gmail.com",
        "password": "yessir",
        "name_first": "Liam",
        "name_last": "Maverick"
        })
    user2_payload = response2.json()
    assert response2.status_code == 200

    response_c = requests.post(config.url + 'channels/create', json={
        "token": user1_payload['token'],
        "name": "FirstChannel",
        "is_public": "True"
        })
    
    channel_payload = response_c.json()
    assert response_c.status_code == 200

    response_j = requests.post(config.url + 'channels/join', json={
        "token": user2_payload['token'],
        "channel_id": channel_payload['channel_id']
    })
    assert response_j.status_code == 200