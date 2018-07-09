#!/usr/bin/env python

import json
from snap.loggers import request_logger as log


def decode_application_json(http_request):
    log.info('>>> Invoking custom request decoder.')
    decoder_output = {'test_json_input_field': 'dummy_value'}
    #decoder_output.update(http_request.get_json())
    return decoder_output