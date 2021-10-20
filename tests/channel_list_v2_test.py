import pytest
import requests
import json
from src import config
from src.channel import auth_register_v1

def test_channel_list_v2_basic(): 
    requests.delete(config.url + 'clear/v1')
    response_j = requests.post(config.url + "auth/register/v2", json={
    "email": "use4r@gmail.com",
    "password": "dummypass",
    "name_first": "jacky",
    "name_last": "zhu"
    })

    response_p = requests.post(config.url + "auth/register/v2", json={
    "email": "pratik7@gmail.com",
    "password": "ronaldo",
    "name_first": "Pratik",
    "name_last": "Napit"
    })

    user_j_payload = response_j.json()
    user_p_payload = response_p.json()
    assert response_j.status_code == 200
    assert response_p.status_code == 200

    response1 = requests.post(config.url + 'channels/create', json={
        "token": user_j_payload['token'],
        "name": "FirstChannel",
        "is_public": "True"
        })
    
    response_cp = requests.post(config.url + 'channels/create', json={
        "token": user_p_payload['token'],
        "name": "IshaChannel",
        "is_public": "True"
        })

    channel_payload = response1.json()
    assert response1.status_code == 200
    assert response_cp.status_code == 200
    assert channel_payload == {"channel_id": 1}


    response2 = requests.get(config.url + 'channels/list', params = {
        'token': user_j_payload['token']
    })

    list_payload = response2.json()
    assert list_payload == [{
        "channel_id": 1,
        "name": "FirstChannel"
    }]

    #testing list all route 
    response3 = requests.get(config.url + 'channels/listall', params = {
        'token': user_j_payload['token']
    })
    listall_payload = response3.json()
    assert listall_payload == [{
        "channel_id": 1,
        "name": "FirstChannel"
    },{
        "channel_id": 2,
        "name": "IshaChannel"
    }]

