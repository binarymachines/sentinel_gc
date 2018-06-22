
#!/usr/bin/env python

 
from snap import snap
from snap import core
import base64
import json
from snap.loggers import transform_logger as log
#from google.cloud import pubsub_v1

MESSAGES = []

def ping_func(input_data, service_objects, **kwargs):
    return core.TransformStatus(json.dumps({'message': 'the SNAP application is alive.'}))


def test_func(input_data, service_objects, **kwargs):
    gcloud_svc = service_objects.lookup('gcloud_config')
    return core.TransformStatus(json.dumps({'inbound_payload': input_data, 'gcloud config': gcloud_svc.config}))


def pubsub_push_func(input_data, service_objects, **kwargs):
    gcloud_svc = service_objects.lookup('gcloud_config')
    if (input_data.get('token', '') !=
            gcloud_svc.config['PUBSUB_VERIFICATION_TOKEN']):
        raise snap.MissingInputFieldException(['request arg "token"'])

    #envelope = json.loads(request.data.decode('utf-8'))
    payload = input_data['message']['data']
    log.info('received inbound pubsub message:')
    log.info(payload)
    MESSAGES.append(payload)
    # Returning any 2xx status indicates successful receipt of the message.
    return core.TransformStatus({})















