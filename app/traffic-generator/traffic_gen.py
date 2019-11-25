#!/usr/bin/env python
import logging
import subprocess
import sys
import os

# Run locust with parameters for load testing
def runLocust():
    frontend_target = os.environ["FRONTEND_TARGET"]
    host = "--host=http://"+ frontend_target
    result = subprocess.run(["locust", "-f", "/app/locustfile.py" , host , "--no-web", "-c 250", "-r 25", "--run-time=1m"], stdout=subprocess.PIPE)
    #print (result)

if __name__ == '__main__':
    logging.info("Running Locust \n")

    runLocust()
    sys.exit(0)
