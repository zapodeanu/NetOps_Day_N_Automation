

# developed by Gabi Zapodeanu, TSA, GPO, Cisco Systems

import json
import requests
import pubnub


from config import PUB_KEY, SUB_KEY, CHANNEL
from config import IOS_XE_PASS, IOS_XE_USER, IOS_XE_HOST
from config import DNAC_URL, DNAC_USER, DNAC_PASS

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from pubnub.callbacks import SubscribeCallback
from pubnub.enums import PNOperationType, PNStatusCategory

from requests.auth import HTTPBasicAuth

from cli import cli
from cli import configure

import netconf_restconf
import dnac_apis


DNAC_AUTH = HTTPBasicAuth(DNAC_USER, DNAC_PASS)

def pubnub_init(device):

    # initialize the channel, with the device hostname

    pnconfig = PNConfiguration()
    pnconfig.subscribe_key = SUB_KEY
    pnconfig.publish_key = PUB_KEY
    pnconfig.ssl = False
    pnconfig.uuid = str(device)
    pubnub = PubNub(pnconfig)
    return pubnub



class MySubscribeCallback(SubscribeCallback):
    def status(self, pubnub, status):
        pass
        # The status object returned is always related to subscribe but could contain
        # information about subscribe, heartbeat, or errors
        # use the operationType to switch on different options
        if status.operation == PNOperationType.PNSubscribeOperation \
                or status.operation == PNOperationType.PNUnsubscribeOperation:
            if status.category == PNStatusCategory.PNConnectedCategory:
                # This is expected for a subscribe, this means there is no error or issue whatsoever
                print('Subscriber connected successfully')
            elif status.category == PNStatusCategory.PNReconnectedCategory:
                # This usually occurs if subscribe temporarily fails but reconnects. This means
                # there was an error but there is no longer any issue
                print('Subscriber drop connectivity and reconnected successfully')
            elif status.category == PNStatusCategory.PNDisconnectedCategory:
                # This is the expected category for an unsubscribe. This means there
                # was no error in unsubscribing from everything
                print('Unsubscribing from everything was successful')
            elif status.category == PNStatusCategory.PNUnexpectedDisconnectCategory:
                # This is usually an issue with the internet connection, this is an error, handle
                # appropriately retry will be called automatically
                print('Connection lost, will try to reconnect')
            elif status.category == PNStatusCategory.PNAccessDeniedCategory:
                pass
                # This means that PAM does allow this client to subscribe to this
                # channel and channel group configuration. This is another explicit error
            else:
                pass
                # This is usually an issue with the internet connection, this is an error, handle appropriately
                # retry will be called automatically
        elif status.operation == PNOperationType.PNSubscribeOperation:
            # Heartbeat operations can in fact have errors, so it is important to check first for an error.
            # For more information on how to configure heartbeat notifications through the status
            # PNObjectEventListener callback, consult <link to the PNCONFIGURATION heartbeart config>
            if status.is_error():
                pass
                # There was an error with the heartbeat operation, handle here
            else:
                pass
                # Heartbeat operation was successful
        else:
            pass
            # Encountered unknown status type

    def presence(self, pubnub, presence):
        pass  # handle incoming presence data

    def message(self, pubnub, message):
        new_message = message.message
        print(str("\nNew message received: " + new_message))
        new_message_list = new_message.split("#")
        device = new_message_list[0]
        if device == DEVICE_HOSTNAME or device == "all":
            command_type = new_message_list[1]
            if command_type == 'config':
                try:
                    command = new_message_list[2:]
                    print('\nConfiguration command received: ' + command +'\n\n')
                    output = configure(command)
                    output_message = "Configuration command successful"
                except:
                    output_message = "Configuration command executed"
                print(output_message)
            else:
                try:
                    command = new_message_list[2]
                    print('\nOperations command received: ' + command +'\n\n')
                    output_message = cli(str(command))
                    output_message = 'Successful'
                except:
                    output_message = 'Not successful'
                print('Show Command result: ', output_message)


def main():
    """
    This application will run locally on the IOS XE device. It will need Guest Shell functionality to be
    configured and be able to reach the Internet.
    The application will listen to a PubNub channel and execute commands, configuration or operational.
    :return:
    """
    global DEVICE_HOSTNAME, DEVICE_LOCATION

    # retrieve the device hostname using NETCONF
    DEVICE_HOSTNAME = netconf_restconf.get_restconf_hostname(IOS_XE_HOST, IOS_XE_USER, IOS_XE_PASS)
    print(str('\nThe device hostname: ' + DEVICE_HOSTNAME))

    # get DNA C AUth JWT token
    dnac_token = dnac_apis.get_dnac_jwt_token(DNAC_AUTH)
    DEVICE_LOCATION = dnac_apis.get_device_location(DEVICE_HOSTNAME, dnac_token)
    print(str("\nDevice Location: " + DEVICE_LOCATION))

    # init the PubNub channel
    pubnub = pubnub_init(DEVICE_HOSTNAME)

    pubnub.add_listener(MySubscribeCallback())
    pubnub.subscribe().channels(CHANNEL).execute()


if __name__ == '__main__':
    main()