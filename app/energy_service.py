from fastapi import FastAPI
from app.request.login.login_request import login
from app.request.energy.energy_request import requestUsageData
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
    return requestUsageData(sessionKeys)

def getDebugResponse():
    with open(debugFilePath) as file:
        return json.load(file)

def debugFileExists():
    return os.path.isfile(debugFilePath)