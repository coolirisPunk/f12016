import socket
import time
import logging

class RequestLogMiddleware(object):
    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        logger = logging.getLogger('django')
        print ("Body request")
        print (request.body)
        if response['content-type'] == 'application/json':
            if getattr(response, 'streaming', False):
                response_body = '<<<Streaming>>>'
            else:
                response_body = response.content
        else:
            response_body = '<<<Not JSON>>>'

        log_data = {
            'user': request.user.pk,
            'remote_address': request.META['REMOTE_ADDR'],
            'server_hostname': socket.gethostname(),
            'request_method': request.method,
            'request_path': request.get_full_path(),
            #'request_body': request.body,
            'response_status': response.status_code,
            'response_body': response_body,

            'run_time': time.time() - request.start_time,
        }
        logger.info(log_data)
        return response