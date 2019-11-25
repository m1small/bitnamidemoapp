import json
import requests
import os
import logging

access_token = ''

refresh_token = os.environ['REFRESH_TOKEN']

## Get Access Token from CSP
def auth():
    
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    url = 'https://console.cloud.vmware.com/csp/gateway/am/api/auth/api-tokens/authorize'
    payload = {"refresh_token": refresh_token }

    response = requests.post(url, data=payload , headers=headers)
    
    if response.status_code == 200:
            print("Success")
            logging.info("Successfully received access token") 
    else:
	 	    logging.error("Failed Retrieving auth token" + str(response.status_code))
    
    data = json.loads(response.content)


    global access_token 
    access_token = data["access_token"]
#    print (access_token)

## Get all the findings within the account 
def all_findings():

    global access_token

    headers = {
        'Content-Type' : 'application/json', 
        'Authorization': 'Bearer {}'.format(access_token)
    }
    payload = "{\n}"
    url = 'https://api.securestate.vmware.com/v1/findings/query'
    response = requests.post(url , data=payload, headers=headers)

    # Fetch the continuation Token
    data = json.loads(response.content)
    continuationToken = data["continuationToken"]

    # Get the entire payload for 1000 objects
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer {}'.format(access_token)
    }

# replace cloud provider key with "AWS" for Amazon web services related violations
    payload = "{\n\t\"filters\": {\n\t\t\"services\": [\"Microsoft.Compute\"]}\n, \n\t\"paginationInfo\":{\n\t\t\"continuationToken\": \"" +  continuationToken + "\",\n\t\t\"pageSize\":1000\n\t}\n}"

    url = 'https://api.securestate.vmware.com/v1/findings/query'
    allFindings = requests.post(url , data=payload, headers=headers)

    print (allFindings)

    return allFindings

## Get all violations related to an ObjectID
def get_violation_by_object(all_findings, objectID):
    violations = []
    
    data = json.loads(all_findings.content)

    #print (data)
## replace ruleId = "5c8c26847a550e1fb6560cab" for Azure and ruleId = "5c8c26417a550e1fb6560c3f" for AWS for port 22 open
## Tim using ruleId = "5c8c267b7a550e1fb6560c9a" for Virtual Machine Disks not Encrypted in Azure 
    for violation in data["results"]:
        if (violation["objectId"] == objectID and violation["level"] == "High" and violation["ruleId"] == "5c8c267b7a550e1fb6560c9a"):
        #if (violation["objectId"] == objectID):
            violations.append(violation)

    if(len(violations) > 0):
        return True
    else:
        return False

# Sets Environment variable within gitlab
def SetGitLabVar(val):

    print ("\nViolation Found \n" + str(val))

    url = "https://gitlab.com/api/v4/projects/13636938/variables/VSS_VIOLATION_FOUND"

    payload = "value="+ str(val)
    headers = {
        'private-token': os.environ["SHRI_PRIVATE_TOKEN"],
        'Content-Type': "application/x-www-form-urlencoded",
        }

    logging.info('Setting GitLab Variable')

    response = requests.request("PUT", url, data=payload, headers=headers)

    print ("GitLab Status Code " + str(response.status_code))

    if response.status_code == 200:
            print("Success")
            logging.info("Successfully updated variable") 
            os.environ["VSS_VIOLATION_FOUND"] = "False"
    else:
	 	    logging.error("Could not update Gitlab variable")
	 	 


## Main Function
if __name__ == '__main__':
    ## Auth
    auth()
    ## Get all Findings
    resp = all_findings()

    ## Get violations based on object IDs
    objects = ["aks-agentpool-18677188-0", "aks-agentpool-18677188-2"]

    violation_found = []
    for objectId in objects:
        ## @TODO - Disable later
        ## has_violation = get_violation_by_object(resp, objectId)
        has_violation = True
        violation_found.append(has_violation)
 
    print("Checking if violations exist \n")
    ## @TODO - fix this later - temporary
    #print(violation_found)
    print("violation found")
    count = 0 
    for violation in violation_found:
        if (violation == True):
            count +=1
            SetGitLabVar(violation)
            break
        else:
            continue
    if (count == 0):
	    logging.info("No Violations Found !!")

