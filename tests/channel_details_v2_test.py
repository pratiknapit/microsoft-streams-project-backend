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
    user_payload = response.json()
    assert response.status_code == 200

    response_c = requests.post(config.url + 'channels/create', json={
        "token": user_payload['token'],
        "name": "FirstChannel",
        "is_public": "True"
        })
    
    channel_payload = response_c.json()
    assert response_c.status_code == 200

    response_det = requests.get(config.url + 'channels/details', params = {
        'token': user_payload['token'],
        'channel_id': channel_payload["channel_id"]
    })

    detail_payload = response_det.json()
    
    assert detail_payload == {
        'name': "FirstChannel",
        'is_public': 'True',
        'owner_members':[{
            'u_id':user_payload['auth_user_id'], 
            "email":"pratik7@gmail.com", 
            'name_first':"Pratik",
            'name_last':"Napit",
            'handle_str':"pratiknapit",
        }],
        'all_members':[{
            'u_id':user_payload['auth_user_id'], 
            "email":"pratik7@gmail.com", 
            'name_first':"Pratik",
            'name_last':"Napit",
            'handle_str':"pratiknapit",
        }]               
        
    }


    