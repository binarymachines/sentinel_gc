
#!/usr/bin/env python

 
from snap import snap
from snap import core
import base64
import json
from snap.loggers import request_logger as log
#from google.cloud import pubsub_v1

MESSAGES = []

def ping_func(input_data, service_objects, **kwargs):
    log.info('### inside ping endpoint. Application is alive.')
    return core.TransformStatus(json.dumps({'message': 'the SNAP application is alive.'}))


def test_func(input_data, service_objects, **kwargs):
    gcloud_svc = service_objects.lookup('gcloud_config')
    return core.TransformStatus(json.dumps({'inbound_payload': input_data, 'gcloud config': gcloud_svc.config}))


def pubsub_push_func(input_data, service_objects, **kwargs):
    gcloud_svc = service_objects.lookup('gcloud_config')
    if (input_data.get('token', '') !=
            gcloud_svc.config['PUBSUB_VERIFICATION_TOKEN']):
        log.info('"token" argument is missing or incorrect.')
        raise snap.MissingInputFieldException(['request arg "token"'])

    log.info('### inside pubsub message handler.')
    return core.TransformStatus(None)


def pubsub_push_alt_func(input_data, service_objects, **kwargs):
    log.info('### inside alternate pubsub message handler.')
    return core.TransformStatus(None)


def noop_func(input_data, service_objects, **kwargs):
    log.info('### a client has accessed the / endpoint.')
    return core.TransformStatus(None)


def noop_get_func(input_data, service_objects, **kwargs):
    log.info('### a client has accessed the / endpoint using HTTP GET.')
    return core.TransformStatus(None)
