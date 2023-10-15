from fastapi import FastAPI
from login import login
from energy_request import request

app = FastAPI(docs_url=None, redoc_url=None)

@app.get('/get')
def get():
    sessionKeys = login()
    return request(sessionKeys)