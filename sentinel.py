
#!/usr/bin/env python

#
# Generated Flask routing module for SNAP microservice framework
#



from flask import Flask, request, Response
from snap import snap
from snap import core
import logging
import json
import argparse
import sys
from snap.loggers import request_logger as log

sys.path.append('/Users/dtaylor/workshop/amc/sentinel_gc')
import s_transforms

f_runtime = Flask(__name__)

if __name__ == '__main__':
    print('starting SNAP microservice in standalone (debug) mode...')
    f_runtime.config['startup_mode'] = 'standalone'
    
else:
    print('starting SNAP microservice in wsgi mode...')
    f_runtime.config['startup_mode'] = 'server'

app = snap.setup(f_runtime)
xformer = core.Transformer(app.config.get('services'))


#-- snap exception handlers ---

xformer.register_error_code(snap.NullTransformInputDataException, snap.HTTP_BAD_REQUEST)
xformer.register_error_code(snap.MissingInputFieldException, snap.HTTP_BAD_REQUEST)
xformer.register_error_code(snap.TransformNotImplementedException, snap.HTTP_NOT_IMPLEMENTED)

#------------------------------



#-- snap data shapes ----------


default = core.InputShape("default")

test_shape = core.InputShape("test_shape")
test_shape.add_field('placeholder', True)
test_shape.add_field('day', True)

event = core.InputShape("event")
event.add_field('token', True)
event.add_field('message', True)

event = core.InputShape("event")
event.add_field('token', True)
event.add_field('message', True)

default = core.InputShape("default")


#------------------------------


#-- snap transform loading ----
xformer.register_transform('ping', default, s_transforms.ping_func, 'application/json')
xformer.register_transform('test', test_shape, s_transforms.test_func, 'application/json')
xformer.register_transform('pubsub_push', event, s_transforms.pubsub_push_func, 'application/json')
xformer.register_transform('pubsub_push_alt', event, s_transforms.pubsub_push_alt_func, 'application/json')
xformer.register_transform('noop', default, s_transforms.noop_func, 'application/json')

#------------------------------



@app.route('/ping', methods=['GET'])
def ping():
    try:
        if app.debug:
            # dump request headers for easier debugging
            log.info('### HTTP request headers:')
            log.info(request.headers)

        input_data = {}                
        input_data.update(request.args)
        
        transform_status = xformer.transform('ping',
                                             core.convert_multidict(input_data),
                                             headers=request.headers)        
        output_mimetype = xformer.target_mimetype_for_transform('ping')

        if transform_status.ok:
            return Response(transform_status.output_data, status=snap.HTTP_OK, mimetype=output_mimetype)
        return Response(json.dumps(transform_status.user_data), 
                        status=transform_status.get_error_code() or snap.HTTP_DEFAULT_ERRORCODE, 
                        mimetype=output_mimetype) 
    except Exception as err:
        log.error("Exception thrown: ", exc_info=1)        
        raise err


@app.route('/test', methods=['GET'])
def test():
    try:
        if app.debug:
            # dump request headers for easier debugging
            log.info('### HTTP request headers:')
            log.info(request.headers)

        input_data = {}                
        input_data.update(request.args)
        
        transform_status = xformer.transform('test',
                                             core.convert_multidict(input_data),
                                             headers=request.headers)        
        output_mimetype = xformer.target_mimetype_for_transform('test')

        if transform_status.ok:
            return Response(transform_status.output_data, status=snap.HTTP_OK, mimetype=output_mimetype)
        return Response(json.dumps(transform_status.user_data), 
                        status=transform_status.get_error_code() or snap.HTTP_DEFAULT_ERRORCODE, 
                        mimetype=output_mimetype) 
    except Exception as err:
        log.error("Exception thrown: ", exc_info=1)        
        raise err


@app.route('/pubsub/push', methods=['POST'])
def pubsub_push():
    try:
        if app.debug:
            # dump request headers for easier debugging
            log.info('### HTTP request headers:')
            log.info(request.headers)

        input_data = {}
        request.get_data()
        input_data.update(core.map_content(request))
        
        transform_status = xformer.transform('pubsub_push', input_data, headers=request.headers)        
        output_mimetype = xformer.target_mimetype_for_transform('pubsub_push')

        if transform_status.ok:
            return Response(transform_status.output_data, status=snap.HTTP_OK, mimetype=output_mimetype)
        return Response(json.dumps(transform_status.user_data), 
                        status=transform_status.get_error_code() or snap.HTTP_DEFAULT_ERRORCODE, 
                        mimetype=output_mimetype) 
    except Exception as err:
        log.error("Exception thrown: ", exc_info=1)        
        raise err


@app.route('/_ah/push-handlers/test', methods=['POST'])
def pubsub_push_alt():
    try:
        if app.debug:
            # dump request headers for easier debugging
            log.info('### HTTP request headers:')
            log.info(request.headers)

        input_data = {}
        request.get_data()
        input_data.update(core.map_content(request))
        
        transform_status = xformer.transform('pubsub_push_alt', input_data, headers=request.headers)        
        output_mimetype = xformer.target_mimetype_for_transform('pubsub_push_alt')

        if transform_status.ok:
            return Response(transform_status.output_data, status=snap.HTTP_OK, mimetype=output_mimetype)
        return Response(json.dumps(transform_status.user_data), 
                        status=transform_status.get_error_code() or snap.HTTP_DEFAULT_ERRORCODE, 
                        mimetype=output_mimetype) 
    except Exception as err:
        log.error("Exception thrown: ", exc_info=1)        
        raise err


@app.route('/', methods=['POST'])
def noop():
    try:
        if app.debug:
            # dump request headers for easier debugging
            log.info('### HTTP request headers:')
            log.info(request.headers)

        input_data = {}
        request.get_data()
        input_data.update(core.map_content(request))
        
        transform_status = xformer.transform('noop', input_data, headers=request.headers)        
        output_mimetype = xformer.target_mimetype_for_transform('noop')

        if transform_status.ok:
            return Response(transform_status.output_data, status=snap.HTTP_OK, mimetype=output_mimetype)
        return Response(json.dumps(transform_status.user_data), 
                        status=transform_status.get_error_code() or snap.HTTP_DEFAULT_ERRORCODE, 
                        mimetype=output_mimetype) 
    except Exception as err:
        log.error("Exception thrown: ", exc_info=1)        
        raise err





if __name__ == '__main__':
    #
    # If we are loading from command line,
    # run the Flask app explicitly
    #
    app.run(host='127.0.0.1', port=5000)

