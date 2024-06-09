from fastapi import FastAPI
from app.request.login.login_request import login
from app.request.energy.energy_request import request_usage_data
import os
import json

app = FastAPI(docs_url=None, redoc_url=None)
debug_file_path = "./get_response.json"

@app.get('/get')
def get():
    if (debug()):
        print('Debug file present')
        return get_debug_response()
    session_keys = login()
    return request_usage_data(session_keys)

def get_debug_response():
    with open(debug_file_path) as file:
        return json.load(file)

def debug():
    return os.path.isfile(debug_file_path)
