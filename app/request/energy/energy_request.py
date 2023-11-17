import json
import requests
from ...constants.constants import usageRequestCookies, genericRequestHeaders, electricUsageRequestJson, waterUsageRequestJson, waterRequestEndpoint, electricRequestEndpoint, RequestMode, uselessResponseKeys

from datetime import date
from datetime import timedelta
# Electric

def doElectricRequest(requestMode: RequestMode):
    electricUsageRequestJson['Mode'] = requestMode.value
    if (requestMode in [RequestMode.halfHour, RequestMode.hour]):
        electricUsageRequestJson['strDate'] = getYesterday()
    return performElectricRequest()

def performElectricRequest():
    electricUsageResponse = requests.post(
        electricRequestEndpoint,
        cookies=usageRequestCookies,
        headers=genericRequestHeaders,
        json=electricUsageRequestJson
    )
    return parseResponse(electricUsageResponse)

def requestElectric():
    return {
        "halfHour": doElectricRequest(RequestMode.halfHour),
        "hour": doElectricRequest(RequestMode.hour),
        "day": doElectricRequest(RequestMode.day),
        "month": doElectricRequest(RequestMode.month)
    }

# Water

def doWaterRequest(requestMode: RequestMode):
    waterUsageRequestJson['Mode'] = requestMode.value
    if (requestMode in [RequestMode.hour]):
        waterUsageRequestJson['strDate'] = getYesterday()
    return performWaterRequest()

def performWaterRequest():
    waterUsageResponse = requests.post(
        waterRequestEndpoint,
        cookies=usageRequestCookies,
        headers=genericRequestHeaders,
        json=waterUsageRequestJson
    )
    return parseResponse(waterUsageResponse)

def requestWater():
    return {
        "hour": doWaterRequest(RequestMode.hour),
        "day": doWaterRequest(RequestMode.day),
        "month": doWaterRequest(RequestMode.month)
    }

# Utility methods
    
def parseResponse(response):
    jsonResponse = json.loads(response.text.replace("\\\"", "\"").replace("\\\"", "\"").replace("\"{\"", "{\"").replace("}\"}", "}}"))['d']
    cleanResponse(jsonResponse)
    return {
        "usageData": jsonResponse['objUsageGenerationResultSetTwo'], # Raw usage data for each timeframe
        "tentativeData": jsonResponse['getTentativeData'] # Accumulated usage data and predictions
    }

def setupRequestParameters(parameters):
    # Setup cookies and csrftoken to perform requests
    usageRequestCookies['ApplicationGatewayAffinityCORS'] = parameters['aga']
    usageRequestCookies['ApplicationGatewayAffinity'] = parameters['aga']
    usageRequestCookies['ASP.NET_SessionId'] = parameters['asi']
    usageRequestCookies['SCP'] = parameters['lt']
    genericRequestHeaders['csrftoken'] = parameters['ct']

# Service calling method

def requestUsageData(requestParameters):
    setupRequestParameters(requestParameters)
    return {
        "electric": requestElectric(),
        "water": requestWater()
    }

def getYesterday():
    yesterday = date.today() - timedelta(days = 1)
    return yesterday.strftime("%x")

def cleanResponse(response: dict):
    # Remove the response keys that provide no information
    for key in uselessResponseKeys:
        removeKey(response, key)

def removeKey(object, keyBeingRemoved):
    # If object is a dict, recursively search over data for keyBeingRemoved
    if (isinstance(object, dict)):
        for listData in list(object):
            if listData == keyBeingRemoved:
                del object[keyBeingRemoved]
            else:
                removeKey(object[listData], keyBeingRemoved)
    # If the object is a list, iterate over each object in the list
    elif (isinstance(object, list)):
        for listData in list(object):
            removeKey(listData, keyBeingRemoved)
