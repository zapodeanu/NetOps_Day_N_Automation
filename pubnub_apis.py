

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems

import json
import requests
import pubnub
import datetime
import time

from config import PUB_KEY, SUB_KEY, CHANNEL

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

def pubnub_init():

    # initialize the channel

    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = SUB_KEY
    pnconfig.publish_key = PUB_KEY
    pnconfig.ssl = False
    pubnub = PubNub(pnconfig)
    return pubnub


def publish_callback(result, status):
    print("\nPublish result: ", result)
    # Handle PNPublishResult and PNStatus


def here_now_callback(result, status):
    if status.is_error():
        # handle error
        return

    for channel_data in result.channels:
        print("\nChannel status now:")
        print("channel: %s" % channel_data.channel_name)
        print("occupancy: %s" % channel_data.occupancy)
    for occupant in channel_data.occupants:
        print("uuid: %s, state: %s" % (occupant.uuid, occupant.state))


def pub_message(command):
    pubnub = pubnub_init()
    # print("\nPubNub Channel Info: ", pubnub)
    pubnub.publish().channel(CHANNEL).message(command).async(publish_callback)
    pubnub.here_now() \
        .channels(CHANNEL) \
        .include_uuids(True) \
        .async(here_now_callback)

"""
pubnub = pubnub_init()
print("\nPubNub Channel Info: ", pubnub)
pubnub.publish().channel(CHANNEL).message('NYC-9300#oper#show ip int bri').async(publish_callback)
pubnub.here_now() \
    .channels(CHANNEL) \
    .include_uuids(True) \
    .async(here_now_callback)
"""