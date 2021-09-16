from os import environ
from dotenv import load_dotenv
import json


def get_fortigate_list():
    load_dotenv()
    ret = []
    for key, value in environ.items():
        if 'FOS_EXTRA_HOST' in key:
            value = json.loads(value)
            ret.append(value)
    return ret


get_fortigate_list()