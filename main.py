from datetime import datetime
import time
import os
import requests
import json
import pymongo

from apscheduler.schedulers.background import BackgroundScheduler

conn = pymongo.MongoClient(host='192.168.12.116', port=27017,
                           username='admin', password='admin', )
db = conn.get_database('onos')

api_url = 'http://192.168.103.229:8181/onos/v1'


def devices():
    print('Get devices: %s' % datetime.now())
    response = web_request(method_name='GET', url=api_url + "/devices", dict_data=None)

    collection = db.get_collection('devices')

    for device in response.get('devices'):
        device['_id'] = device['id']
        collection.update_one({'_id': device['_id']}, {'$set': device}, upsert=True)


def ports():
    print('Get ports: %s' % datetime.now())

    devices_collection = db.get_collection('devices')
    ports_collection = db.get_collection('ports')
    device_list = devices_collection.find()

    for device in device_list:
        response = web_request(method_name='GET', url=api_url + "/devices/" + device['_id'] + "/ports", dict_data=None)
        for port in response.get('ports'):
            port['_id'] = port['element'] + "_" + port['port']
            ports_collection.update_one({'_id': port['_id']}, {"$set": port}, upsert=True)


def web_request(method_name, url, dict_data, is_urlencoded=True):
    method_name = method_name.upper()
    if method_name not in ('GET', 'POST'):
        raise Exception('method_name is GET or POST plz...')

    if method_name == 'GET':
        response = requests.get(url=url, auth=('onos', 'rocks'), params=dict_data)
    elif method_name == 'POST':
        if is_urlencoded is True:
            response = requests.post(url=url, auth=('onos', 'rocks'), data=dict_data,
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
        else:
            response = requests.post(url=url, data=json.dumps(dict_data), headers={'Content-Type': 'application/json'})

    dict_meta = {'status_code': response.status_code, 'ok': response.ok, 'encoding': response.encoding,
                 'Content-Type': response.headers['Content-Type']}
    if 'json' in str(response.headers['Content-Type']):
        return {**dict_meta, **response.json()}
    else:
        return {**dict_meta, **{'text': response.text}}


if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(devices, 'interval', seconds=10)
    scheduler.add_job(ports, 'interval', seconds=10)
    scheduler.start()
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        while True:
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()