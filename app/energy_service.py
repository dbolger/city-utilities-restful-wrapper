from fastapi import FastAPI
from app.login.login import login
from app.energy_request.energy_request import request

app = FastAPI(docs_url=None, redoc_url=None)

@app.get('/get')
def get():
    sessionKeys = login()
    return request(sessionKeys)