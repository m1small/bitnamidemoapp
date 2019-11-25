
# Front-End Service 


## Requirements

**Node - version 10.15.0** - DO NOT USE ANY VERSION which is not LTS


Install Node only from PPA - https://websiteforstudents.com/install-the-latest-node-js-and-nmp-packages-on-ubuntu-16-04-18-04-lts/

Latest version of Chrome/Safari 

**WARNING:** Not Tested on FireFox

Use developer tools in browser to look at console logs for client side


## Code Structure 

**app.js**  - To be used only for NodeJs server configuration and adding mount points
        - When integrating with new services, remember to add a mount point here. 
        - DO NOT modify the packages and configuration already added


**public/** - Contains all the html file

        - every html file has a <script> tag under which the AJAX scripts are added
        - follow the index.html for some of the naming conventions. Especially for the Top navigation bar and the footer
        - make changes as necessary for your service (like redirecting to another page, loading a different html etc)

**public/js/client.js** - Contains all the js functions for handling certain front end actions

**services/{service_name}** - Add index.js file here for every service that frontend needs to interact with
                        - currently services/users/index.js has sample code for making call to another backend service 
                        - requests library is being used to handle the calls to other services
                        - Refer to API doc or contact the author of the service for which the calls are being made to
                          make changes as necessary 

package.json - contains list of packages
             - if using any new package, use the command npm install package_name --save
             - this will update the json

.gitignore


## Run the app

1. Export the following Environment variables 

Replace the values based on your environment. Ensure that all the other services are running before starting the front-end app.

       export PORT=8080 (default value is 3000)
       export USERS_HOST=0.0.0.0
       export CATALOG_HOST=0.0.0.0
       export CART_HOST=0.0.0.0
       export ORDER_HOST=0.0.0.0
       export USERS_PORT=8081    
       export CATALOG_PORT=8082
       export CART_PORT=5000
       export ORDER_PORT=6000
   
 The default values for all the env with _PORT is 80


2. Install all the package(s)
     
      ``` npm install ```

3. Start the App 

        npm start

The current user service will set a cookie ```logged_in``` in the browser. This cookie contains ths User ID returned from the user service

Use this ID to make calls to other services (Eventually it will be replaced with JWT)

The default users are available as JSON file in the user microservice 

Follow the README of these services for more info on setup

Default Registered Users :
 
username: **eric**
password: vmware1!

username: **elaine**
password: vmware1!

username: **han**
password: vmware1!

username: **phoebe**
password: vmware1!

Currently there is also a **guest** user - if you dont login into the account

## API

All the calls from other services will work directly with the Front-End Service

## Additional Resource 

https://github.com/request/request

https://stackoverflow.com/questions/26721994/return-json-body-in-request-nodejs?rq=1


