from os import environ
from dotenv import load_dotenv
import json


def get_fortigate_list():
    """ Finds all environment varibles starting with 'FOS_EXTRA_HOST' and creates a list of dictionaries
    to pass along to the collect_endpoints.py module."""
    load_dotenv()
    ret = []
    for key, value in environ.items():
        if 'FOS_EXTRA_HOST' in key:
            value = json.loads(value)
            ret.append(value)
    return ret
