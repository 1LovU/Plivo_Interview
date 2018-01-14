import requests
import logging
import sys
from requests.packages.urllib3.exceptions import InsecureRequestWarning,SNIMissingWarning, InsecurePlatformWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
requests.packages.urllib3.disable_warnings(InsecurePlatformWarning)
requests.packages.urllib3.disable_warnings(SNIMissingWarning)


def api_get(url, config_dict):
    l = logging.getLogger()
    url = url.format(**config_dict)        # Using DICT to insert the param values.
    auth_id = config_dict['auth_id']
    auth_token = config_dict['auth_token']

    # I needed to use Main auth_id and token because it was giving authorization error for Pricing_API
    if 'Pricing' in url:
        auth_id = config_dict['main_auth_id']
        auth_token = config_dict['main_auth_token']

    try:

        l.debug(f"\tURL :: {url}")
        res = requests.get(url, auth=(auth_id, auth_token), headers={"content-type": "application/json"}, verify=True)
        print('======================================================')
        print('Logger Msg, URL Hit :: ', res.status_code, res.reason)
        l.debug(f"\tres.status :: {res.status_code}\nres.reason :: {res.reason}\nres.json :: {res.json()}")
        if res.reason == 'OK':
            return res.json()
        else:
            print('Error in Hitting the URL.')
            l.debug(f"Error in Hitting the URL.")
            sys.exit(1)

    except Exception as e:
        print(e)
        print('Error hitting the URL.')
        l.debug(f"\tError :: {e}")
        sys.exit(1)


def api_post(url, config_dict):
    l = logging.getLogger()
    url = url.format(**config_dict)         # Using DICT to insert the param values.
    auth_id = config_dict['auth_id']
    auth_token = config_dict['auth_token']

    msg = {
            "src": config_dict['src_ID'],
            "dst": config_dict['dst_ID'],
            "text": config_dict['text_message']
           }
    msg = str(msg).replace("'", '"')         # Converting DICT to JSON format

    try:
        l.debug(f"\tURL :: {url}")
        l.debug(f"\tMSG :: {msg}")
        res = requests.post(url, msg, auth=(auth_id, auth_token), headers={"content-type": "application/json"}, verify=False)
        print('======================================================')
        print('Logger Msg, URL Hit :: ', res.status_code, res.reason)
        l.debug(f"\tres.status :: {res.status_code}\nres.reason :: {res.reason}\nres.json :: {res.json()}")

        if res.reason == 'ACCEPTED':             # On Success URL hit.
            return res.json()
        else:
            print('Error in Hitting the URL.')
            l.debug(f"Error in Hitting the URL.")
            sys.exit(1)

    except Exception as e:
        print(e)
        print('Error hitting the URL.')
        l.debug(f"\tError :: {e}")
        sys.exit(1)


