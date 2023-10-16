import json
import requests
from ...constants.constants import usageRequestCookies, genericRequestHeaders, electricUsageRequestJson, waterUsageRequestJson, waterRequestEndpoint, electricRequestEndpoint

# Electric

def dayElectricRequest():
    electricUsageRequestJson['Mode'] = 'D'
    return performElectricRequest()

def monthElectricRequest():
    electricUsageRequestJson['Mode'] = 'M'
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
        "day": dayElectricRequest(),
        "month": monthElectricRequest()
    }

# Water

def dayWaterRequest():
    waterUsageRequestJson['Mode'] = 'D'
    return performWaterRequest()

def monthWaterRequest():
    waterUsageRequestJson['Mode'] = 'M'
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
        "day": dayWaterRequest(),
        "month": monthWaterRequest()
    }

# Utility methods
    
def parseResponse(response):
    # such an icky response from an endpoint
    jsonResponse = json.loads(response.text.replace("\\\"", "\"").replace("\\\"", "\"").replace("\"{\"", "{\"").replace("}\"}", "}}"))['d']
    # TODO: Remove useless data from response
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

