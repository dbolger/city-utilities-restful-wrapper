import requests
import re
from constants import loginPageHeaders, loginRequestJson, genericRequestHeaders, loginPageUri, loginRequestEndpoint

def login():
    # Grab generated session keys from viewing the webpage
    aga, asi, ct = grabRequiredKeys()
    # Perform a login request using keys found on the page and JSON data (credentials)
    lt = performLoginRequest(aga, asi, ct)
    # Return the keys required to make endpoint calls
    return {
        "lt": lt,
        "aga": aga,
        "asi": asi,
        "ct": ct
    }


def grabRequiredKeys():
    loginPageResponse = requests.get(loginPageUri, headers=loginPageHeaders)
    affinityMatcher = re.compile("CORS=(.+?);")
    affinityResults = affinityMatcher.search(loginPageResponse.headers['Set-Cookie'])
    appGatewayAffinity = affinityResults.group(1)

    aspNetSessionIdMatcher = re.compile("ASP\.NET\_SessionId=(.+?);")
    aspnetResults = aspNetSessionIdMatcher.search(loginPageResponse.headers['Set-Cookie'])
    aspNetSessionId = aspnetResults.group(1)

    csrfMatcher = re.compile("id=\"hdnCSRFToken\" value=\"(.+)\"")
    csrfResults = csrfMatcher.search(loginPageResponse.text)
    csrfToken = csrfResults.group(1)
    return appGatewayAffinity, aspNetSessionId, csrfToken

def performLoginRequest(appGatewayAffinity, aspNetSessionId, csrfToken):
    loginRequestCookies = {
        'ApplicationGatewayAffinityCORS': appGatewayAffinity,
        'ApplicationGatewayAffinity': appGatewayAffinity,
        'ASP.NET_SessionId': aspNetSessionId,
    }

    genericRequestHeaders['csrftoken'] = csrfToken

    loginResponse = requests.post(
        loginRequestEndpoint,
        cookies=loginRequestCookies,
        headers=genericRequestHeaders,
        json=loginRequestJson,
    )

    scpMatcher = re.compile("SCP=(.{36});")
    scpSearchResults = scpMatcher.search(loginResponse.headers['Set-Cookie'])
    loginToken = scpSearchResults.group(1)
    return loginToken
