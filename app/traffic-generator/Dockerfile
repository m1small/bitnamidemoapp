FROM bitnami/python:3.7

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

#test
#ENTRYPOINT [python3]
CMD ["python3", "traffic_gen.py"]
