FROM bitnami/node:10
COPY ./app/front_end/package*.json ./
RUN npm install
COPY ./app/front_end/ .
EXPOSE 3000
CMD [ "npm", "start" ]
#test
