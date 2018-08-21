#!/usr/bin/env python

"""
Exporter for my utilities usage. Currently just heat usage, but soon to be electicity etc
"""

import os
import requests
import time

from prometheus_client import start_http_server, Gauge

def get_heat_usage(heat_org, heat_account, heat_token):
    """
    Queries coheat for the meter reading, taking a coheat org, account ID and a bearer token for the API
    """
    url = 'https://api.client.coheat.co.uk/api/customer/v1/organization/{}/account/{}/meters'.format(heat_org, heat_account)
    headers = {'Authorization': 'Bearer {}'.format(heat_token)}
    r = requests.get(url, headers=headers)
    data = r.json()
    meter_readings = {}
    for meter in data['meters']:
        meter_readings[meter['meter_uuid']] = meter['end_reading']['value']
    return meter_readings

HEAT_USAGE = Gauge('heat_usage', 'The amount of heat in kWh I\'ve used', ['uuid'])

def process_metrics():
    usage = get_heat_usage(os.environ['HEAT_ORG'], os.environ['HEAT_ACCOUNT'], os.environ['HEAT_TOKEN'])
    for meter_uuid, usage_kwh in usage.iteritems():
        HEAT_USAGE.labels(meter_uuid).set(usage_kwh)

def main():
    start_http_server(8000)
    while True:
        process_metrics()
        time.sleep(300)

if __name__ == '__main__':
    main()
