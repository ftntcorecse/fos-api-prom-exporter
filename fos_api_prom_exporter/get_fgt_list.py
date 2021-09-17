from os import environ
from dotenv import load_dotenv
import json


def get_fortigate_list():
    """ Finds all environment varibles starting with 'FOS_EXTRA_HOST_', such as FOS_EXTRA_HOST_1
    or FOS_EXTRA_HOST_NEWYORK and creates a list of dictionaries
    to pass along to the collect_endpoints.py module."""
    # load env vars
    load_dotenv()
    # create an empty list to append to
    ret = []
    # loop through all the environment variables looking for "FOS_EXTRA_HOST" in the key name.
    for key, value in environ.items():
        if 'FOS_EXTRA_HOST' in key:
            # if found, load the JSON from that env var and append it to the return list
            value = json.loads(value)
            ret.append(value)
    return ret
