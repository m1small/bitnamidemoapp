var request = require('request')
var express = require("express")
var async = require("async")
var http = require('http')

var app = express()

var endpoints = require('../services')


// Handles post call to /login
app.post("/login", function(req, res, next) {
  
    // @todo - Replace the uri paramter 
    // uri - needs to be created dynamically. This is only for local testing
    // var options = {
    //   uri: 'http://0.0.0.0:8088/login',
    //   method: 'POST',
    //   body: req.body,
    //   json: true
    // };

    console.log(endpoints.usersUrl)

    var options = {
        uri: endpoints.usersUrl + "/login",
        method: 'POST',
        body: req.body,
        json: true
      };
  
    // Logs data to server side console
    console.log("Posting " + JSON.stringify(req.body));

    // Leverages request library
    request(options, function(error, response, body) {
        if (error) {
          return next(error);
        }
        // for debugging only
        console.log(response.statusCode)

        if (response.statusCode == 200) {
            var logged_in = body.token
            console.log(logged_in)
            res.cookie('logged_in', logged_in, "/")
            res.writeHead(200)
            res.write(JSON.stringify(body))
            res.end();
        } 
        
        else {
            console.log("Error with log in: " + req.body.username);
            res.status(response.statusCode);
            res.write(JSON.stringify(response.statusMessage))
            res.end();
        }

    }); // end of request

}); // End of app.post('/login')


app.get("/users/:id", function(req, res, next) {
  
    // @todo - Replace the uri paramter 
    // uri - needs to be created dynamically. This is only for local testing
    var options = {
      uri: endpoints.usersUrl + "/users/" + req.params.id,
      method: 'GET',
      json: true
    };

    // Leverages request library
    request(options, function(error, response, body) {
        if (error) {
          return next(error);
        }

        if (response.statusCode == 200) {
            console.log('printing from within request')
            res.writeHead(200)
            res.write(JSON.stringify(body))
            res.end();
        } 
        else {
            res.status(response.statusCode);
            res.write(JSON.stringify(response.statusMessage))
            res.end();
        }

    }); // end of request

}); 

  module.exports = app;