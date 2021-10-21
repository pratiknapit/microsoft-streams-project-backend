import pytest
import requests
import json
from src import config

def test_channel_addowner_removeowner_v2_functionality():
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
    user2_payload = response.json()
    assert response2.status_code == 200

    response3 = requests.post(config.url + 'channels/create', json={
        "token": user1_payload['token'],
        "name": "FirstChannel",
        "is_public": "True"
    })
    channel_payload = response3.json()
    assert response3.status_code == 200

    response4 = requests.post(config.url + 'channel/addowner', json={
        "token": user1_payload['token'],
        "channel_id": channel_payload['channel_id'],
        "u_id": user2_payload['auth_user_id']
    })
    assert response4.status_code == 200

    response4 = requests.post(config.url + 'channel/removeowner', json={
        "token": user1_payload['token'],
        "channel_id": channel_payload['channel_id'],
        "u_id": user2_payload['auth_user_id']
    })
    assert response4.status_code == 200


    
    