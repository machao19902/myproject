from oslo_config import cfg

# Register options for the service
OPTS = [
    cfg.StrOpt('paste_config',
               default="api-paste.ini",
               help="Configuration file for WSGI definition of API."),
    cfg.IntOpt('port',
               default=8043,
               help="The port for the myproject API server. (port value)."),
    ]
