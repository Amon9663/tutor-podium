from glob import glob
import os
import requests
import logging

from .__about__ import __version__

HERE = os.path.abspath(os.path.dirname(__file__))

templates = os.path.join(HERE, "templates")

# Handle Errors when Sending Query to server --> All `tutor` commands run this program regardless of whether the plugin is enabled or disabled
try:
    # Send request to AWS to get IP address
    response = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4', timeout=0.01)

    # TODO: Find way to validate IP ADDRESS
    IP_ADDRESS = response.text

    config = {
    "add": {
        "AWS_HOST_IP": IP_ADDRESS,
        "AWS_IP_LOOKUP": True,
    },
    # "set": {
    #     "ENABLE_SMTP": False
    # }

    # Does not automatically append plugin name to key name in config.yml as per docs (Potential bug)
    # "set":{
    #     "AWS_IP_LOOKUP": False
    # },
    # Does not automatically append plugin name to key name in config.yml as per docs (Potential bug)
    # "defaults": {
    #     "AWS_IP_LOOKUP": True
    # }
    }
except requests.exceptions.RequestException as e:
    pass

hooks = {}


def patches():
    all_patches = {}
    for path in glob(os.path.join(HERE, "patches", "*")):
        with open(path) as patch_file:
            name = os.path.basename(path)
            content = patch_file.read()
            all_patches[name] = content
    return all_patches
