# Payment Service

## API calls

GET '/live'

Returns 200, 'live'

PUT '/pay'
{
  "card": {
    "number": "1234", //must be a multiple of 4 digits
    "expYear": "2020",
    "expMonth": "01",
    "ccv" : "123"
  },
	"total": "123"
}

All of the above values are required

Service is currently hardcoded to port 9000

## Successful output

200 SUCCESS response with body JSON

{
  success: 'true',
  message: 'transaction successful',
  amount: total,
  transactionID: tID
}


## Validations

1. All 4 keys in the JSON blob have non-NULL values
2. cardNum is a multiple of 4 digits (4,8,12,16, etc)
3. Card is not expired

## Dockerfile

Dockerfile exists in repo
Build and run making sure port maps to 9000 [Exposed port]

docker build -t <username>/payment .
docker run -p 9000:9000 -d <username>/payment
