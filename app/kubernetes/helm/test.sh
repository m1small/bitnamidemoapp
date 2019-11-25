#!/bin/bash

set -eu -o pipefail

readonly baseUrl="${1:-http://127.0.0.1:3000}"

exitCode=0

logDetails() {
  if [ "${DEBUG:-0}" = "1" ] ; then
    cat
  else
    cat >/dev/null
  fi
}

# pass if the command returned zero exit code ; fail otherwise
passFail() {
  local label="$1"
  shift

  if "$@" 2>&1 | logDetails ; then
    echo "PASS: ${label}"
  else
    echo "FAIL: ${label}"
    exitCode=1
  fi
}

# fail if the command returned zero exit code ; pass otherwise
failPass() {
  local label="$1"
  shift

  if "$@" 2>&1 | logDetails ; then
    echo "FAIL: ${label}"
    exitCode=1
  else
    echo "PASS: ${label}"
  fi
}

# helper to avoid calling curl directly
curlAjax() {
  local url="${1}"
  shift
  curl "${baseUrl}${url}" -H 'Content-Type: application/json; charset=UTF-8' -H 'Accept: */*' --fail "$@"
}

# curl + check if a result is present in jq
curlAjaxJqPresent() {
  local jq="${1}"
  shift
  local url="${1}"
  shift
  if [ "$(curlAjax ${url} "$@" | jq "${jq}" | wc -c)" -lt 6 ] ; then
    return 1
  else
    return 0
  fi
}

testUser() {
  passFail "user: valid" curlAjax /login --data-binary $'{"username":"eric","password":"vmware1\u21"}' 
  failPass "user: invalid" curlAjax /login --data-binary $'{"username":"none","password":"vmware1\u21"}' 
}

testProducts() {
  passFail "products: correct" curlAjax /products
  passFail "products: non-empty" curlAjaxJqPresent .data /products 
}

testCart() {
  failPass "cart: empty" curlAjaxJqPresent .cart /cart/items/guest
  passFail "cart: add item" curlAjax /cart/item/add/guest --data-binary $'{"name":"TEST","price":"1","shortDescription":"TEST","quantity":1,"itemid":"5d2d79a4d7e0d05bd2ff76b3"}'
  passFail "cart: has items" curlAjaxJqPresent .cart /cart/items/guest
  passFail "cart: remove item" curlAjax /cart/item/modify/guest --data-binary '{"itemid":"5d2d79a4d7e0d05bd2ff76b3","quantity":0}'
  failPass "cart: empty" curlAjaxJqPresent .cart /cart/items/guest
}

testOrder() {
  local orderData=$'{"userid":"guest","firstname":"Test","lastname":"User","total":"34.99","address":{"street":"","city":"","zip":"","state":"AL","country":"USA"},"email":"","delivery":"tractor","card":{"type":"amex","number":"1234567812345678","ccv":"123","expMonth":"01","expYear":"2029"},"cart":"[{\\"itemid\\":\\"5d2d79a4d7e0d05bd2ff76b1\\",\\"name\\":\\"Water Bottle\\",\\"price\\":\\"34.99\\",\\"quantity\\":1,\\"shortDescription\\":\\"The last Water Bottle you\'ll ever buy\u21\\"}]"}'
  passFail "order: call" curlAjax /order/add/guest --data-binary "${orderData}"
  passFail "order: order_id" curlAjaxJqPresent .order_id /order/add/guest --data-binary "${orderData}"
  passFail "order: payment succeeded" curlAjaxJqPresent '[.payment][] | select(.success == "true")' /order/add/guest --data-binary "${orderData}"
}

testUser
testProducts
testCart
testOrder

exit ${exitCode}
