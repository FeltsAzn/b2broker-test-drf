FROM python:3.11

RUN apt-get update -y && apt-get install -y default-libmysqlclient-dev gcc

# Trying  to wait of mysql initialization in container
ENV CONNECTION_TRYING_AMOUNT=10

WORKDIR app/
COPY requirements.txt .
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt

COPY deploy/run.sh .
RUN chmod +x run.sh
COPY deploy/check_db_connection.py .
COPY app/ .

CMD ./run.sh
