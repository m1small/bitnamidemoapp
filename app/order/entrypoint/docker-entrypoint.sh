#!/bin/sh

echo $ORDER_DB_HOST
echo $ORDER_DB_USERNAME
echo $ORDER_DB_PASSWORD
echo $ORDER_DB_PORT

until mongo --host $ORDER_DB_HOST --port $ORDER_DB_PORT --username $ORDER_DB_USERNAME --password=$ORDER_DB_PASSWORD --authenticationDatabase admin --eval "printjson(db.serverStatus())"; do
  >&2 echo "mongo is unavailable - sleeping" then
  sleep 1
done

echo "Apply flask now"
python3 order.py
exec "$@"
