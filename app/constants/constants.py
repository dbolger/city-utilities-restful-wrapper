from app.request.login.credentials import *
from enum import Enum

# Useless response key/pairs
uselessResponseKeys = ['DemandColorCode', 'UsageDelvcolorCode', 'UsageReccolorCode',
               'UsageColorCode', 'SoFarColorCode', 'ExpectedUsageColorCode',
               'PeakLoadColorCode', 'AverageColorCode', 'LoadFactorColorCode',
               'HighestColorCode', 'IsOnlyAMI', 'Skey', 'AccountNumber',
               'UpToDecimalPlaces', 'UsageCycle', 'PeakLoad', 'LoadFactor',
               'DemandValue', 'UsageRecValue', 'WeatherUsageDate']

# Possible energy request modes
class RequestMode(Enum):
    halfHour = 'MI'
    hour = 'H'
    day = 'D'
    month = 'M'

# Shared
genericRequestHeaders = {
    # set csrftoken
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.9,la;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json; charset=UTF-8',
    'DNT': '1',
    'Origin': 'https://myaccount.cityutilities.net',
    'Pragma': 'no-cache',
    'Referer': 'https://myaccount.cityutilities.net/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'isajax': '1',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}
################################################################
# Login
loginPageHeaders = {
    # no setting needed
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'en-US,en;q=0.9,la;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'DNT': '1',
    'Pragma': 'no-cache',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

loginRequestJson = {
    # no setting needed
    'username': username,
    'password': password,
    'rememberme': False,
    'calledFrom': 'LN',
    'ExternalLoginId': '',
    'LoginMode': '1',
    'utilityAcountNumber': '',
}
################################################################
# Usage

usageRequestCookies = {
    # set the following:
    # ApplicationGatewayAffinityCORS
    # ApplicationGatewayAffinity
    # ASP.NET_SessionId
    # SCP
    'HomeInfoStatus': 'JTvtoeyEoms3X37GlOdLTgqBBOA=',
    'ClientTimeZone': 'fHqu9CayhyHioR9w4GOAmCGNfuI=',
    'ClientTimeId': 'YHGrE6y4VMYjLFGwicApVDP8CQ==',
    'Language_code': 'FAeYmCxPzfN/s2ABidwmk2yR',
    'IsModernStyle': 'BTvtoZ0jt+/Sat+a9yZhduxHX60=',
    'Language_Name': 'FCf/qJCh2GYtR4LS0rM5/Zpmrv4n89w=',
    'UName': uName,
}

electricUsageRequestJson = {
    # Set Mode
    'UsageOrGeneration': '1',
    'Type': 'K',
    'hourlyType': 'H',
    'SeasonId': '',
    'weatherOverlay': 0,
    'usageyear': '',
    'MeterNumber': electricMeterNumber,
    'DateFromDaily': '',
    'DateToDaily': '',
}

waterUsageRequestJson = {
    # Set Mode
    "Type":"W",
    "hourlyType":"H",
    "seasonId":"",
    "weatherOverlay":0,
    "usageyear":"",
    "MeterNumber": waterMeterNumber,
    "DateFromDaily":"",
    "DateToDaily":"",
    "isNoDashboard":True
}

################################################################
# Endpoints/URIs

waterRequestEndpoint = 'https://myaccount.cityutilities.net/Portal/Usages.aspx/LoadWaterUsage'
electricRequestEndpoint = 'https://myaccount.cityutilities.net/Portal/Usages.aspx/LoadUsage'
loginRequestEndpoint = 'https://myaccount.cityutilities.net/Portal/Default.aspx/validateLogin'
loginPageUri = 'https://myaccount.cityutilities.net/Portal/default.aspx'