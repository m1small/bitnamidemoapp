FROM bitnami/python:3.7
MAINTAINER Bill Shetti "billshetti@gmail.com"
ENV ORDER_DB_HOST="localhost"
ENV ORDER_DB_PORT="27017"
ENV ORDER_DB_PASSWORD=""
ENV ORDER_DB_USERNAME=""
ENV MONGO_AUTH_DB="admin"
ENV PAYMENT_HOST="localhost"
ENV PAYMENT_PORT="9000"

# needed for mongo client
RUN install_packages mongodb-clients

COPY ./app/order/requirements.txt /app/requirements.txt
RUN pip3 install -r requirements.txt

ADD . /app
COPY /app/order/entrypoint/docker-entrypoint.sh /usr/local/bin/
RUN chmod 777 /usr/local/bin/docker-entrypoint.sh
RUN ln -s /usr/local/bin/docker-entrypoint.sh /app # backwards compat

EXPOSE 80
EXPOSE 5000
ENTRYPOINT ["docker-entrypoint.sh"]
#CMD ["python3", "cart.py"]
#
