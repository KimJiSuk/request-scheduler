## Request Api, insert Mongo DB Service

### Overview
http://192.168.103.229:8181/onos/v1/docs/

request api in 192.168.103.229:8181 and insert Mongo DB

#### Requirements
Python 3+

#### Config
[config.ini](http://192.168.101.197/jskim/request-scheduler/-/blob/master/config.ini)
```
[DB]
HOST = 192.168.12.116
PORT = 27017
DATABASE = onos
USERNAME = admin
PASSWORD = admin

[API]
URL = http://192.168.103.229:8181/onos/v1
```

#### Usage

install & run
```
pip install -r requirements.txt
python main.py
```

#### Docker Usage

build & run
```
docker build -t mobigen/request-scheduler .
docker run -d --name request-scheduler mobigen/request-scheduler
```