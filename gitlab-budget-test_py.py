#!/usr/bin/python
#Made some small changes
import json
import pickle
import os
import sys
import datetime
import string
import subprocess
import requests


#Logging initialization
import logging
from logging.config import dictConfig
from logging.handlers import SysLogHandler

DEFAULT_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'loggers': {
        '': {
            'level': 'INFO',
        },
        'another.module': {
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(DEFAULT_LOGGING)

api_url_base="https://chapi.cloudhealthtech.com/olap_reports/custom/6116033433314?api_key=62666453-6065-45da-9755-d0ed96911da6"
headers={'Content-Type': 'application/json'}

def getPolicy():

    f=open('policy.json', "r")
    output=json.loads(f.read())
    f.close()

    return output

def getGCPCost():

    payload={'interval':'monthly'}

    response=requests.get(api_url_base, headers=headers) #add params=payload for other parameters

    if response.status_code == 200:
        output = json.loads(response.content.decode('utf-8'))
        f=open('rawoutput.txt', "w+")
        f.write(json.dumps(output, indent=5, sort_keys=True))
        f.close()
    else:
        return 0

    return output

def checkCost(output, budget):

    if float(output["data"][0][0][0]) > budget:
        amountOver=(float(output["data"][0][0][0])-budget)
        return amountOver
    else:
        return -1

def dumpinFile(overBudget):

    try:
        f=open('overbudget.txt', "w+")
    except error as e:
        print("Error opening file", error)
    
    try:
        f.write(str(overBudget))
    except error as e:
        print("Error writing file", error)
        
    f.close()


if __name__ == '__main__':

    if sys.argv[1]:
        TOKEN=sys.argv[1]
    else:
        TOKEN="TTT"

    url = "https://gitlab.com/api/v4/projects/13636938/variables/OVERAGE"

    githeaders = {}
    githeaders['Content-Type']="application/json"
    githeaders['Authorization']="Bearer "+TOKEN
    print("githeader is", githeaders)

    policy=getPolicy()
    print(policy)
    budget=int(policy['budget']['limit'])
#    logging.info("in main")
    output=getGCPCost()
    if output != 0:
        overBudget=checkCost(output, budget)
        if overBudget > 2000:
            dumpinFile(overBudget)
            print("OVER so wrote file overbudget")
            payload='{"value":"OVER"}'
            response = requests.request("PUT", url, data=payload, headers=githeaders)
        else:
            payload='{"value":"UNDER"}'
            print("NOT writing file since its UNDER")
            response = requests.request("PUT", url, data=payload, headers=githeaders)
    else:
        print("found issue")
