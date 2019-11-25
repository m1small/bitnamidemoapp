FROM bitnami/node:10
COPY ./app/payment/package*.json ./
RUN npm install
COPY ./app/payment/ .
EXPOSE 9000
CMD [ "npm", "start" ]
#test
