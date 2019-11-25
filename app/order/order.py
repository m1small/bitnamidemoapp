#!/usr/bin/python

#general imports
import json
import pickle
import os
import random
import sys
import datetime
import string
import uuid

#Logging initialization
import logging
from logging.config import dictConfig
from logging.handlers import SysLogHandler

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi'],
        'propagate': True,
    }
})

#errorhandler for specific responses
class FoundIssue(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

#Uncomment below to turnon statsd
#from statsd import StatsClient
#statsd = StatsClient(host='localhost',
#                     port=8125,
#                     prefix='fitcycle-api-server',
#                     maxudpsize=512)



#initializing flask
from flask import Flask, render_template, jsonify, flash, request
app = Flask(__name__)
app.debug=True


@app.errorhandler(FoundIssue)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

#initializing mongo on localhost and port 27017
#If error terminates process- entire order is shut down
from os import environ

if environ.get('ORDER_DB_USERNAME') is not None:
    if os.environ['ORDER_DB_USERNAME'] != "":
        mongouser=os.environ['ORDER_DB_USERNAME']
    else:
        mongouser=''
else:
    mongouser=''

if environ.get('ORDER_DB_HOST') is not None:
    if os.environ['ORDER_DB_HOST'] != "":
        mongohost=os.environ['ORDER_DB_HOST']
    else:
        mongohost='localhost'
else:
    mongohost='localhost'

if environ.get('ORDER_DB_PORT') is not None:
    if os.environ['ORDER_DB_PORT'] != "":
        mongoport=os.environ['ORDER_DB_PORT']
    else:
        mongoport=27017
else:
    mongoport=27017

if environ.get('ORDER_DB_PASSWORD') is not None:
    if os.environ['ORDER_DB_PASSWORD'] != "":
        mongopassword=os.environ['ORDER_DB_PASSWORD']
    else:
        mongopassword=''
else:
    mongopassword=''

if environ.get('PAYMENT_HOST') is not None:
    if os.environ['PAYMENT_HOST'] != "":
        paymenthost=os.environ['PAYMENT_HOST']
    else:
        paymenthost='localhost'
else:
    paymenthost='localhost'

if environ.get('PAYMENT_PORT') is not None:
    if os.environ['PAYMENT_PORT'] != "":
        paymentport=os.environ['PAYMENT_PORT']
    else:
        paymentport='9000'
else:
    paymentport='9000'


if environ.get('ORDER_PORT') is not None:
    if os.environ['ORDER_PORT'] != "":
        orderport=os.environ['ORDER_PORT']
    else:
        orderport='5000'
else:
    orderport='5000'

#initializing requests
import requests
from requests.auth import HTTPBasicAuth

paymenturi='http://'+str(paymenthost)+':'+str(paymentport)




def testPayment():

    paymentup=0

    try:
        paymentreq = requests.get(paymenturi+'/live')
        paymentup=1
        app.logger.info("payment service up %s", paymentreq.status_code)
    except Exception as ex:
        paymentup=0
        app.logger.error('Error connecting to payment service %s', ex)

    return paymentup


import pymongo
from pymongo import MongoClient
from pymongo import errors as mongoerrors

try:
    client=MongoClient(host=mongohost, port=int(mongoport), username=mongouser, password=mongopassword)
    app.logger.info('initiated mongo connection %s', client)
    db=client.orderDB
    orders=db.order_collection
    orders.delete_many({})
except Exception as ex:
    app.logger.error('Error for mongo connection %s', ex)
    exit('Failed to connect to mongo, terminating')

#Generates a random string for order id
def randomString(stringLength=15):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

#initialization of redis with fake data from the San Francisco legal offices of Shri, Dan and Bill SDB.
def insertInitialData():

    app.logger.info('inserting order')

    order = { "userid":"1234",
      "firstname":"Bill",
      "lastname": "Shetti",
      "address":{
        "street":"Test Street",
        "city":"San Francisco",
        "zip":"94127",
        "state": "CA",
        "country":"USA"},
      "email":"test@gmail.com",
      "delivery":"UPS/FEDEX",
      "card":{
        "type":"amex",
        "number":"1234123412341234",
        "expMonth":"12",
        "expYear":"221",
        "ccv":"123"
      },
      "cart":[
        {"id":"1234", "description":"redpants", "quantity":"1", "price":"4"},
        {"id":"5678", "description":"bluepants", "quantity":"1", "price":"4"},
      ],
      "date":datetime.datetime.utcnow(),
      "total":"100",
      "_id":str(uuid.uuid1()),
#      "_id":randomString(),
      "paid":"transaction id - success - 0 failed"
    }


    try:
        order_id=orders.insert_one(order).inserted_id
        app.logger.info("Inserted order # %s", order_id)
    except Exception as e:
        app.logger.error("Could not insert initial data into mongo")


#Gets specific order
def getOrder(orderid):

    document = orders.find_one({"_id":orderid})
    if document != None:
        unpacked_data = document
        app.logger.info('got data')
    else:
        app.logger.info('empty - no data for key %s', orderid)
        unpacked_data = 0

    return unpacked_data

#http call to gets all Items from a cart (userid)
#If successful this returns the cart and items, if not successfull (the user id is non-existant) - 204 returned

#@statsd.timer('getOrderUser')
@app.route('/order/<userid>', methods=['GET'])
def getUserOrders(userid):

    app.logger.info('getting all orders for user %s', userid)

    totalOrders = []
    order={}

    for document in orders.find({"userid":str(userid)}):
        order=document
        totalOrders.append(order)
        order={}

    return jsonify({'all orders': totalOrders})


#http call to get all orders and their values
#@statsd.timer('getAllOrders')
@app.route('/order/all', methods=['GET'])
def getAllOrders():
    app.logger.info('getting orders')

    totalOrders = []
    order={}

    for document in orders.find():
        order=document
        totalOrders.append(order)
        order={}

    return jsonify({'all orders': totalOrders})


#http call to create and order - doesn't look for another order. It essentially adds an order to the database
#once the order is paid (via payment the field "paid" is set to yes/no)
@app.route('/order/add/<userid>', methods=['GET', 'POST'])
def createOrder(userid):
    paymentup=0
    content = request.json

#    content['_id']=randomString()
    content['_id']=str(uuid.uuid1())
    content['date']=str(datetime.datetime.utcnow())
    content['paid']="pending"
    transactionId="pending"
    order_id=0

    paymentres={}
    paymentPayload={}
    paymentPayload['card']=content['card']
    paymentPayload['firstname']=content['firstname']
    paymentPayload['lastname']=content['lastname']
    paymentPayload['address']=content['address']
    paymentPayload['total']=content['total']

    app.logger.info('creating order for %s with following contents %s',userid, json.dumps(content))

    paymentup=testPayment()

    try:
        order_id=orders.insert_one(content).inserted_id
        app.logger.info("Initial insert of order %s", order_id)
    except Exception as e:
        app.logger.error("Could not insert initial data into mongo %s", e)
        raise FoundIssue(str(e), status_code=500)

    try:
        if paymentup==0:
            app.logger.info("Payment service is down will not process")
            paymentres=makeFakePayment(paymentPayload)
            transactionId=paymentres['transactionID']
        else:
            app.logger.info("Making call to real payment service")
            paymentres=makePayment(paymentPayload)
            transactionId=paymentres['transactionID']
        content['paid']=transactionId
        try:
#            if (order_id !=0 and transactionId != string.empty):
            if (order_id != 0):
                app.logger.info("Updating order # %s with transaction id %s", order_id, transactionId)
                orders.update_one({"_id": order_id},{"$set":{"paid": transactionId}})
            else:
                app.logger.info("Issue updating order - it was never added properly to orderDB")
        except Exception as e:
            app.logger.error("Could not update order into mongo")
            raise FoundIssue(str(e), status_code=204)

    except Exception as e:
        app.logger.error("Issue with making call to payment")
        raise FoundIssue(str(e), status_code=500)

    return jsonify({"userid":userid, "order_id":order_id, "payment":paymentres})


#placeholder for call to payment
def makeFakePayment(paymentPayload):

    transactionId=randomString()

    paymentres={"success":"false", "message":"Payment service is down", "amount":paymentPayload['total'], "transactionID": transactionId}

    return paymentres

def makePayment(paymentPayload):

    app.logger.info("Sending payload %s:", paymentPayload)
    headers = {'content-type': 'application/json'}
    data=json.dumps(paymentPayload)
    paymentreq = requests.post(paymenturi+'/pay', headers=headers, data=data)
    #app.logger.info("result is", paymentreq.status_code, json.loads(paymentreq.json()))
    paymentres=paymentreq.json()

    if (paymentreq.status_code==200 or paymentreq.status_code==400 or paymentreq.status_code==401 or paymentreq.status_code==402):

        app.logger.info("got a known result from payment %s", paymentres)
    else:
        papp.logger.info("got an unknown result from payment %s", paymentres)


    return paymentres

#baseline route to check is server is live ;-)
@app.route('/')
def hello_world(name=None):
	return render_template('hello.html')


if __name__ == '__main__':

    testPayment()
    insertInitialData() #initialize the database with some baseline
    app.run(host='0.0.0.0', port=orderport)
