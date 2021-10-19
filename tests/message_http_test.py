'''
from json import dumps
from flask import Flask, request
from src.error import InputError
from src.data_store import password_check, email_check, email_repeat_check
from src.auth import auth_register_v1, auth_login_v1, auth_logout
'''
