import collections

import grpc

from ua_parser import user_agent_parser


class _ClientCallDetails(
    collections.namedtuple(
        '_ClientCallDetails',
        ('method', 'timeout', 'metadata', 'credentials')),
        grpc.ClientCallDetails):
    pass


class CustomGrpcInterceptor(grpc.UnaryUnaryClientInterceptor,
                            grpc.UnaryStreamClientInterceptor):

    def __init__(self, request):
        self.request = request

    def intercept_unary_stream(self, continuation, client_call_details, request):
        new_detail = _ClientCallDetails(client_call_details.method, client_call_details.timeout,
                                        (('ip', '777'),), client_call_details.credentials)
        return continuation(new_detail, request)

    def intercept_unary_unary(self, continuation, client_call_details, request):
        # add user ip to metadata
        new_detail = _ClientCallDetails(client_call_details.method,
                                        client_call_details.timeout,
                                        (('ip', get_client_ip(self.request)),
                                         ('device', get_device(self.request))),
                                        client_call_details.credentials)
        return continuation(new_detail, request)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_device(request):
    user_agent = user_agent_parser.Parse(request.META.get('HTTP_USER_AGENT'))
    device = user_agent['device']['family'] + '_' + user_agent['user_agent']['family']
    return device
