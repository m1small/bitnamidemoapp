var express = require('express'),
  app = express(),
  port = process.env.PAYMENT_PORT;
  if (!port) {
    port = 9000;
  }
  body = require('body-parser');

const uuidv4 = require('uuid/v4');

app.use(body.urlencoded({ extended: true }));
app.use(body.json());

//Liveness test via GET
app.get('/live', function (req,res) {
  res.send('live');
})

//POST to process 'payment'
app.post('/pay', function (req, res) {
  console.log('POST call to /pay');
  console.log(req.body);
  //check card number
  card = req.body.card;
  d = new Date();
  cardNum = card.number;
  curYear = d.getFullYear();
  curMonth = d.getMonth()+1;
  expYear = Number(card.expYear);
  expMonth = Number(card.expMonth);
  ccv = card.ccv;
  total = Number(req.body.total);
  if (!cardNum || !expYear || !expMonth || !ccv || !total) {
    console.log('payment failed due to incomplete info');
    res.status(400).send({
      success: 'false',
      status: '400',
      message: 'missing required data',
      amount: '0',
      transactionID: '-1'
    })
  }
  else if(cardNum.length % 4 != 0) {
    console.log('payment failed due to bad card number');
    return res.status(400).send({
      success: 'false',
      status: '400',
      message: 'not a valid card number',
      amount: '0',
      transactionID: '-2'
    });
  }
  //check expiry
  else if ((expYear < curYear) || (expYear == curYear && (expMonth < curMonth))) {
    console.log('payment failed due to expired card');
    return res.status(400).send({
      success: 'false',
      status: '400',
      message: 'card is expired',
      amount: '0',
      transactionID: '-3'
    });
  }
  //process payment
  else {
    console.log('payment processed successfully');
    tID = uuidv4();
    return res.status(200).send({
      success: 'true',
      status: '200',
      message: 'transaction successful',
      amount: total,
      transactionID: tID
    });
  }
})

app.listen(port);

console.log('payment service started on: ' + port);
