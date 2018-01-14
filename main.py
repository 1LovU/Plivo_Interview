# ==============================================================================================
# This is Plivo Assignment code base with SMS API hit and checking for successful transaction
# Author ::     Amit Kumar Yadav
# mail id ::    theamitcoder@gmail.com
# Date ::       14-JAN-2018
# ===============================================================================================
import json
import os
import sys
import logging
from time import sleep
from configparser import RawConfigParser
from url_hit import api_get, api_post

# changing current DIR
os.chdir(os.path.dirname(sys.argv[0]))

# Creating a log file
logging.basicConfig(filename='plivo.log', level=logging.DEBUG)
l = logging.getLogger()
l.debug("\n=====================================================================================\n")
l.debug("Working directory: %s", os.getcwd())


try:
    config = RawConfigParser()
    config.read('api.ini')                      # Fetching configuration params,api,res

    main_auth_id = config['PARAM']['main_auth_id']
    main_auth_token = config['PARAM']['main_auth_token']
    auth_id = config['PARAM']['auth_id']
    auth_token = config['PARAM']['auth_token']
    country_iso = config['PARAM']['country_iso']
    text_message = config['PARAM']['text_message']

    account_api = config['API']['account_api']
    account_res = config['RES']['account_res']
    account_res = json.loads(account_res)       # changing STR to JSON / Testing purpose only.

    pricing_api = config['API']['pricing_api']
    pricing_res = config['RES']['pricing_res']
    pricing_res = json.loads(pricing_res)       # changing STR to JSON / Testing purpose only.

    send_sms_api = config['API']['send_sms_api']
    send_sms_res = config['RES']['send_sms_res']
    send_sms_res = json.loads(send_sms_res)      # changing STR to JSON / Testing purpose only.

    detail_single_sms_api = config['API']['detail_single_sms_api']
    detail_single_sms_res = config['RES']['detail_single_sms_res']
    detail_single_sms_res = json.loads(detail_single_sms_res)      # changing STR to JSON / Testing purpose only.


except Exception as e:
    print(str(e))
    input('Please make sure the config file "api.ini" is there in folder with variables names and header.')
    sys.exit(1)


def main(argv):
    global account_api, pricing_api, send_sms_api, detail_single_sms_api

    # check to see if there are exactly two numbers entered on command line.
    if len(argv) != 3:
        print('Enter two Numbers by space separated in command line.')
        l.debug('EXIT : Enter two Numbers by space separated in command line.')
        sys.exit(1)

    src_id = argv[1]
    dst_id = argv[2]

    # Checking if the entered numbers are integer. Exit if False
    if not (src_id.isdigit() and dst_id.isdigit()):
        print('Numbers must be integers, not string.')
        l.debug(f'EXIT : Numbers must be integers, not string. \nNumbers : {src_id}  {dst_id}')
        sys.exit(1)

    # Variable dict to use in string formatting. This way, I don't need to remember the sequence of params.
    config_dict = {'auth_id': auth_id,
                   'auth_token': auth_token,
                   'main_auth_id': main_auth_id,
                   'main_auth_token': main_auth_token,
                   'country_iso': country_iso,
                   'src_ID': src_id,
                   'dst_ID': dst_id,
                   'text_message': text_message,
                   }
    l.debug(f'config_dict :: {config_dict}')

    # ==========================================================================================
    # Process Zero :: Account detail before sending SMS, save the initial cash credits .
    account_res = api_get(account_api, config_dict)
    l.debug(f'account_res :: {account_res}')

    initial_cash_credits = account_res['cash_credits']
    config_dict['initial_cash_credits'] = initial_cash_credits
    print(f'initial_cash_credits ::\t{initial_cash_credits}')
    l.debug(f'initial_cash_credits :: {initial_cash_credits}')
    sleep(1)

    # ==========================================================================================
    # Process One :: HIT SMS API and save the message_uuid
    send_sms_res = api_post(send_sms_api, config_dict)
    l.debug(f'send_sms_res :: {send_sms_res}')

    message_uuid = send_sms_res['message_uuid'][0]
    config_dict['message_uuid'] = message_uuid      # Updating the message_uuid in DICT for future use.
    print(f'message_uuid ::\t{message_uuid}')
    l.debug(f'message_uuid :: {message_uuid}')
    print('======================================================')
    print('Please Wait while data is getting updated to the server,\nWaiting time : 200 Seconds')
    print('======================================================')
    sleep(200)  # Had to add sleep 200 seconds because data was not updated to the server even on first 100 seconds

    # ==========================================================================================
    # Process Two :: HIT SMS detail API and save the total_rate in DICT
    detail_single_sms_res = api_get(detail_single_sms_api, config_dict)
    l.debug(f'detail_single_sms_res :: {detail_single_sms_res}')

    total_rate = detail_single_sms_res['total_rate']
    config_dict['total_rate'] = total_rate  # Updating the total_rate in DICT for future use.
    print(f'total_rate ::\t{total_rate}')
    l.debug(f'total_rate :: {total_rate}')
    sleep(1)

    # ==========================================================================================
    # Process Three :: HIT Pricing API and save the outbound_rate in DICT
    pricing_res = api_get(pricing_api, config_dict)
    l.debug(f'pricing_res :: {pricing_res}')

    outbound_rate = pricing_res['message']['outbound']['rate']
    config_dict['outbound_rate'] = outbound_rate  # Updating the total_rate in DICT for future use.
    print(f'outbound_rate ::\t{outbound_rate}')
    l.debug(f'outbound_rate :: {outbound_rate}')

    # ===========================================================================================
    # Process Four : Check if outbound rate is equal to the deducted rate or not.
    print('======================================================')
    if outbound_rate == total_rate:
        print('Success : Outbound rate is Equal to the rate deducted.')
    else:
        print('Error : Outbound rate is not Equal to the rate deducted.')
        #sys.exit(1)

    # ==========================================================================================
    # Process Five :: HIT Account detail API and compare with initial cash credit
    account_res = api_get(account_api, config_dict)
    l.debug(f'account_res :: {account_res}')

    final_cash_credits = account_res['cash_credits']
    config_dict['final_cash_credits'] = final_cash_credits

    print(f'final_cash_credits ::\t{final_cash_credits}')
    l.debug(f'final_cash_credits :: {final_cash_credits}')

    print('=================================')
    credit_deducted = float(initial_cash_credits) - float(final_cash_credits)
    credit_deducted = float("%.5f" % credit_deducted)

    print(f'Credit deducted :: {credit_deducted}')
    l.debug(f'credit_deducted :: {credit_deducted}')

    config_dict['credit_deducted'] = credit_deducted
    l.debug(f'config_dict :: {config_dict}')

    print('=================================')

    if not (float(credit_deducted) - float(outbound_rate)):
        print('Transaction Successful...')
        l.debug('Transaction Successful...')
    else:
        print('Transaction Unsuccessful...')
        l.debug('Transaction Unsuccessful...')


if __name__ == '__main__':
    main(sys.argv)
