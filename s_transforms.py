
#!/usr/bin/env python

 
from snap import snap
from snap import core
import base64
import json
from snap.loggers import transform_logger as log
#from google.cloud import pubsub_v1



def ping_func(input_data, service_objects, **kwargs):
    return core.TransformStatus(json.dumps({'message': 'the SNAP application is alive.'}))

def test_func(input_data, service_objects, **kwargs):

    gcloud_svc = service_objects.lookup('gcloud_config')
    return core.TransformStatus(json.dumps({'inbound_payload': input_data, 'gcloud config': gcloud_svc.config}))
















