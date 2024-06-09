import json
import requests
from ...constants.constants import usage_request_cookies, generic_request_headers, electric_usage_request_json, water_usage_request_json, water_request_endpoint, electric_request_endpoint, RequestMode, useless_response_keys

from datetime import date
from datetime import timedelta
# Electric

def do_electric_request(request_mode: RequestMode):
    electric_usage_request_json['Mode'] = request_mode.value
    if (request_mode in [RequestMode.halfHour, RequestMode.hour]):
        electric_usage_request_json['strDate'] = get_yesterday_date()
    return perform_electric_request()

def perform_electric_request():
    electric_usage_response = requests.post(
        electric_request_endpoint,
        cookies=usage_request_cookies,
        headers=generic_request_headers,
        json=electric_usage_request_json
    )
    return parse_response(electric_usage_response)

def request_electric():
    return {
        "halfHour": do_electric_request(RequestMode.halfHour),
        "hour": do_electric_request(RequestMode.hour),
        "day": do_electric_request(RequestMode.day),
        "month": do_electric_request(RequestMode.month)
    }

# Water

def do_water_request(requestMode: RequestMode):
    water_usage_request_json['Mode'] = requestMode.value
    if (requestMode in [RequestMode.hour]):
        water_usage_request_json['strDate'] = get_yesterday_date()
    return perform_water_request()

def perform_water_request():
    water_usage_response = requests.post(
        water_request_endpoint,
        cookies=usage_request_cookies,
        headers=generic_request_headers,
        json=water_usage_request_json
    )
    return parse_response(water_usage_response)

def request_water():
    return {
        "hour": do_water_request(RequestMode.hour),
        "day": do_water_request(RequestMode.day),
        "month": do_water_request(RequestMode.month)
    }

# Utility methods
    
def parse_response(response):
    json_response = json.loads(response.text.replace("\\\"", "\"").replace("\\\"", "\"").replace("\"{\"", "{\"").replace("}\"}", "}}"))['d']
    clean_response(json_response)
    return {
        "usageData": json_response['objUsageGenerationResultSetTwo'], # Raw usage data for each timeframe
        "tentativeData": json_response['getTentativeData'] # Accumulated usage data and predictions
    }

def setup_request_params(parameters):
    # Setup cookies and csrftoken to perform requests
    usage_request_cookies['ApplicationGatewayAffinityCORS'] = parameters['aga']
    usage_request_cookies['ApplicationGatewayAffinity'] = parameters['aga']
    usage_request_cookies['ASP.NET_SessionId'] = parameters['asi']
    usage_request_cookies['SCP'] = parameters['lt']
    generic_request_headers['csrftoken'] = parameters['ct']

# Service calling method

def request_usage_data(request_params):
    setup_request_params(request_params)
    return {
        "electric": request_electric(),
        "water": request_water()
    }

def get_yesterday_date():
    yesterday = date.today() - timedelta(days = 1)
    return yesterday.strftime("%x")

def clean_response(response: dict):
    # Remove the response keys that provide no information
    for key in useless_response_keys:
        remove_key(response, key)

def remove_key(object, key_to_remove):
    # If object is a dict, recursively search over data for keyBeingRemoved
    if (isinstance(object, dict)):
        for list_data in list(object):
            if list_data == key_to_remove:
                del object[key_to_remove]
            else:
                remove_key(object[list_data], key_to_remove)
    # If the object is a list, iterate over each object in the list
    elif (isinstance(object, list)):
        for list_data in list(object):
            remove_key(list_data, key_to_remove)
