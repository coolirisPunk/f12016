from django.utils.decorators import decorator_from_middleware

from .middleware import RequestLogMiddleware
import logging
from django.utils.timezone import now


class RequestLogViewMixin(object):
    """
    Adds RequestLogMiddleware to any Django View by overriding as_view.
    """

    @classmethod
    def as_view(cls, *args, **kwargs):
        view = super(RequestLogViewMixin, cls).as_view(*args, **kwargs)
        view = decorator_from_middleware(RequestLogMiddleware)(view)
        return view


class LoggingMixin(object):
    """Mixin to log requests"""
    log_data = {}
    logger = logging.getLogger('django')
    def initial(self, request, *args, **kwargs):
        """Set current time on request"""
        # get data dict
        try:
            data_dict = request.data.dict()
        except AttributeError:  # if already a dict, can't dictify
            data_dict = request.data

        # get IP
        ipaddr = request.META.get("HTTP_X_FORWARDED_FOR", None)
        if ipaddr:
            # X_FORWARDED_FOR returns client1, proxy1, proxy2,...
            ipaddr = ipaddr.split(", ")[0]
        else:
            ipaddr = request.META.get("REMOTE_ADDR", "")

        # save to log
            self.log_data['requested_at'] = now()
            self.log_data['path'] = request.path
            self.log_data['remote_addr'] = ipaddr
            self.log_data['host'] =request.get_host()
            self.log_data['method'] = request.method
            self.log_data['query_params'] = request.query_params.dict()
            self.log_data['data'] = data_dict


        # regular intitial, including auth check
        super(LoggingMixin, self).initial(request, *args, **kwargs)

        # add user to log after auth
        user = request.user
        if user.is_anonymous():
            user = None
        self.log_data['log_user'] = user


    def finalize_response(self, request, response, *args, **kwargs):
        # regular finalize response
        response = super(LoggingMixin, self).finalize_response(request, response, *args, **kwargs)

        # compute response time
        response_timedelta = now() - self.log_data['requested_at']
        response_ms = int(response_timedelta.total_seconds() * 1000)

        self.log_data['response'] = response.rendered_content
        self.log_data['status_code'] = response.rendered_content
        self.log_data['response_ms'] = response_ms
        # save to log
        self.logger.info(self.log_data)

        # return
        return response