from fastapi import FastAPI
from app.login.login import login
from app.energy_request.energy_request import request
import os
import json

app = FastAPI(docs_url=None, redoc_url=None)
debugFilePath = "./get_response.json"

@app.get('/get')
def get():
    if (debugFileExists()):
        print('Debug file present')
        return getDebugResponse()
    sessionKeys = login()
    return request(sessionKeys)

def getDebugResponse():
    with open(debugFilePath) as file:
        return json.load(file)

def debugFileExists():
    return os.path.isfile(debugFilePath)