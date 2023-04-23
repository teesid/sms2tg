#!/usr/bin/env python

"""\
Forward sms to Telegram
"""

from __future__ import print_function

import logging
import requests
import config
import argparse

from gsmmodem.modem import GsmModem

def tg_send(text):
    requests.post(
        '{0}{1}/sendMessage'.format(config.BOT_API_URL, config.TOKEN),
        data = {'chat_id':config.CHAT_ID, 'text':text}
    )

def handle_sms(sms, sim_name = None):
    #print(u'== SMS message received ==\nFrom: {0}\nTime: {1}\nMessage:\n{2}\n'.format(sms.number, sms.time, sms.text))
    print(sms.text)
    print('Forwarding to TG...')
    tg_send(u'From: {0}\nTo: {1}\nMessage: {2}'.format(sms.number, sim_name, sms.text))
    print('Sent to TG.\n')

def main(args):
    print('Initializing modem...')
    # Uncomment the following line to see what the modem is doing:
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.DEBUG)
    modem = GsmModem(args.device,
                     args.baud,
                     smsReceivedCallbackFunc = lambda sms: handle_sms(sms, args.name))
    modem.smsTextMode = False
    modem.connect(args.pin)
    try:
        print('Processing old received SMS messages...')
        modem.processStoredSms()
        print('Waiting for SMS messages...')
        modem.rxThread.join(2**31) # Specify a (huge) timeout so that it essentially blocks indefinitely, but still receives CTRL+C interrupt signal
    finally:
        modem.close()

def get_args():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--device',
                        type = str,
                        default = '/dev/ttyUSB2',
                        help = 'eg. /dev/ttyUSB2')
    parser.add_argument('-b', '--baud',
                        type = int,
                        default = 115200,
                        help = 'The baud rate. Defaults to 115200.')
    parser.add_argument('-p', '--pin',
                        type = str,
                        help = 'The SIM card PIN (optional).')
    parser.add_argument('-n', '--name',
                        type = str,
                        help = 'The name for the sim.')

    return parser.parse_args()

if __name__ == '__main__':
    args = get_args()
    main(args)
