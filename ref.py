# -*- coding: utf8 -*-
__author__ = 'Aaron'
error_status = {
    200: "OK",
    304: "Not_Modified",
    400: "Bad_Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not_Found",
    406: "Not_Acceptable",
    410: "Gone",
    420: "Enhance_Your_Calm",
    422: "Unprocessable_Entity",
    429: "Too_Many_Requests",
    500: "Internal_Server_Error",
    502: "Bad_Gateway",
    503: "Service_Unavailable",
    504: "Gateway_timeout"
}

non_printing_chars = {
    '&amp;':    "&",
    '&lt;':     '<',
    '&gt;':     '>',
    '&nbsp;':   '   ',
    '&quot;':   '"',
    '\n': '  '
}