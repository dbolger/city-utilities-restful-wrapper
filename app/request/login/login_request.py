import requests
import re
from ...constants.constants import login_page_headers, login_request_json, generic_request_headers, login_page_uri, login_request_endpoint

s = requests.session()

def login():
    # Grab generated session keys from viewing the webpage
    aga, asi, ct = grab_required_keys()
    # Perform a login request using keys found on the page and JSON data (credentials)
    lt = perform_login_request(aga, asi, ct)
    # Return the keys required to make endpoint calls
    return {
        "lt": lt,
        "aga": aga,
        "asi": asi,
        "ct": ct
    }


def grab_required_keys():
    login_page_response = s.get(login_page_uri, headers=login_page_headers)
    affinity_matcher = re.compile("CORS=(.+?);")
    affinity_results = affinity_matcher.search(login_page_response.headers['Set-Cookie'])
    app_gateway_affinity = affinity_results.group(1)

    asp_net_session_id_matcher = re.compile("ASP\.NET\_SessionId=(.+?);")
    asp_net_results = asp_net_session_id_matcher.search(login_page_response.headers['Set-Cookie'])
    asp_net_session_id = asp_net_results.group(1)

    csrf_matcher = re.compile("id=\"hdnCSRFToken\" value=\"(.+)\"")
    csrf_results = csrf_matcher.search(login_page_response.text)
    csrf_token = csrf_results.group(1)
    s.cookies.clear()
    return app_gateway_affinity, asp_net_session_id, csrf_token

def perform_login_request(app_gateway_affinity, asp_net_session_id, csrf_token):
    login_request_cookies = {
        'ApplicationGatewayAffinityCORS': app_gateway_affinity,
        'ApplicationGatewayAffinity': app_gateway_affinity,
        'ASP.NET_SessionId': asp_net_session_id,
    }

    generic_request_headers['csrftoken'] = csrf_token

    login_response = s.post(
        login_request_endpoint,
        cookies=login_request_cookies,
        headers=generic_request_headers,
        json=login_request_json,
    )

    scp_matcher = re.compile("SCP=(.{36});")
    scp_results = scp_matcher.search(login_response.headers['Set-Cookie'])
    login_token = scp_results.group(1)
    s.cookies.clear()
    return login_token
