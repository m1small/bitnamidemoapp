var request = require('request')
var express = require("express")
var async = require("async")
var http = require('http')
var endpoints = require('../services')
var app = express()


app.post("/order/add/:userid", function(req, res, next){

    console.log("Sending to order for user " + req.params.userid);
   

    var options = {
        uri: endpoints.orderUrl + '/order/add/' + req.params.userid,
        method: 'POST',
        body: req.body,
        json: true
    };

    console.log("Posting body to order service " + JSON.stringify(req.body));

    request(options, function(error, response, body){
        if (error) {
            return next(error);
        }

      // for debugging only
      console.log('Order status ' + response.statusCode )

      if(response.statusCode == 200) {
          console.log('Sending Info from order service')
          res.writeHead(200);
          res.write(JSON.stringify(body))
          res.end();
      } else {
          res.status(response.statusCode);
          res.write(JSON.stringify(response.statusMessage));
          res.end();
      }


    }); // end of request

    
});


module.exports = app;