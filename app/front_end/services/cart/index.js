var request = require('request')
var express = require("express")
var async = require("async")
var http = require('http')
var endpoints = require('../services')
var app = express()


app.post("/cart/item/add/:userid", function(req, res, next){

    console.log("Adding item to cart userid " + req.params.userid);
   

    var options = {
        uri: endpoints.cartUrl + '/cart/item/add/' + req.params.userid,
        method: 'POST',
        body: req.body,
        json: true
    };

    console.log("Posting body to cart service " + JSON.stringify(req.body));

    request(options, function(error, response, body){
        if (error) {
            return next(error);
        }

      // for debugging only
      console.log('Cart item add status ' + response.statusCode )

      if(response.statusCode == 200) {
          res.writeHead(200);
          res.end();
      } else {
          res.status(response.statusCode);
          res.write(JSON.stringify(response.statusMessage));
          res.end();
      }


    }); // end of request

    
});

app.post("/cart/item/modify/:userid", function(req, res, next) {

    var options = {
        uri: endpoints.cartUrl + '/cart/item/modify/' + req.params.userid,
        method: 'POST',
        body: req.body,
        json: true
    };

    request(options, function(error, response, body){
        if (error) {
            return next(error);
        }

      // for debugging only
      console.log('Cart item deleted status ' + response.statusCode )

      if(response.statusCode == 200) {
          res.writeHead(200);
          res.end();
      } else {
          res.status(response.statusCode);
          res.write(JSON.stringify(response.statusMessage));
          res.end();
      }


    }); // end of request


});


app.get("/cart/items/:userid", function(req, res, next){

    var options = {
        uri: endpoints.cartUrl + '/cart/items/' + req.params.userid,
        method: 'GET',
        json: true
    };

    request(options, function(error, response, body){
            if (error) {
                return next(error);
            }
    
          // for debugging only
        //   console.log(JSON.stringify(body))
          console.log('Cart item get status ' + response.statusCode )
    
          if(response.statusCode == 200) {
              res.writeHead(200);
              res.write(JSON.stringify(body))
              res.end();
          } else {
              res.status(response.statusCode);
              console.log(response.statusMessage)
              res.write(JSON.stringify(response.statusMessage));
              res.end();
          }
    })

});

app.get("/cart/clear/:userid", function(req, res, next){

    var options = {
        uri: endpoints.cartUrl + '/cart/clear/' + req.params.userid,
        method: 'GET',
        json: true
    };

    request(options, function(error, response, body){
            if (error) {
                return next(error);
            }
    
          // for debugging only
        //   console.log(JSON.stringify(body))
          console.log('Cart clear status ' + response.statusCode )
    
          if(response.statusCode == 200) {
              res.writeHead(200);
              //res.write(JSON.stringify(body))
              res.end();
          } else {
              res.status(response.statusCode);
              console.log(response.statusMessage)
              res.write(JSON.stringify(response.statusMessage));
              res.end();
          }
    })

});


app.get("/cart/total/:userid", function(req, res, next){

    var options = {
        uri: endpoints.cartUrl + '/cart/total/' + req.params.userid,
        method: 'GET',
        json: true
    };

    request(options, function(error, response, body){
            if (error) {
                return next(error);
            }
    
          // for debugging only
        //   console.log(JSON.stringify(body))
          console.log('Cart total status ' + response.statusCode )
    
          if(response.statusCode == 200) {
              res.writeHead(200);
              res.write(JSON.stringify(body))
              res.end();
          } else {
              res.status(response.statusCode);
              console.log(response.statusMessage)
              res.write(JSON.stringify(response.statusMessage));
              res.end();
          }
    })

});


module.exports = app;