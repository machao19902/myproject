from oslo_config import cfg
import oslo_messaging
from oslo_messaging import serializer as oslo_serializer

DEFAULT_URL = "__default__"
TRANSPORTS = {}
_SERIALIZER = oslo_serializer.JsonPayloadSerializer()


def setup():
    oslo_messaging.set_transport_defaults('myproject')


def get_transport(url=None, optional=False, cache=True):
    """Initialise the oslo_messaging layer."""
    global TRANSPORTS, DEFAULT_URL
    cache_key = url or DEFAULT_URL
    transport = TRANSPORTS.get(cache_key)
    if not transport or not cache:
        try:
            transport = oslo_messaging.get_transport(cfg.CONF, url)
        except (oslo_messaging.InvalidTransportURL,
                oslo_messaging.DriverLoadFailure):
            if not optional or url:
                # NOTE(sileht): oslo_messaging is configured but unloadable
                # so reraise the exception
                raise
            return None
        else:
            if cache:
                TRANSPORTS[cache_key] = transport
    return transport


def get_rpc_server(transport, topic, endpoint):
    """Return a configured oslo_messaging rpc server."""
    cfg.CONF.import_opt('host', 'ceilometer.service')
    target = oslo_messaging.Target(server=cfg.CONF.host, topic=topic)
    serializer = oslo_serializer.RequestContextSerializer(
        oslo_serializer.JsonPayloadSerializer())
    return oslo_messaging.get_rpc_server(transport, target,
                                         [endpoint], executor='threading',
                                         serializer=serializer)


def get_rpc_client(transport, retry=None, **kwargs):
    """Return a configured oslo_messaging RPCClient."""
    target = oslo_messaging.Target(**kwargs)
    serializer = oslo_serializer.RequestContextSerializer(
        oslo_serializer.JsonPayloadSerializer())
    return oslo_messaging.RPCClient(transport, target,
                                    serializer=serializer,
                                    retry=retry)


def get_batch_notification_listener(transport, targets, endpoints,
                                    allow_requeue=False,
                                    batch_size=1, batch_timeout=None):
    """Return a configured oslo_messaging notification listener."""
    return oslo_messaging.get_batch_notification_listener(
        transport, targets, endpoints, executor='threading',
        allow_requeue=allow_requeue,
        batch_size=batch_size, batch_timeout=batch_timeout)


def get_notifier(transport, publisher_id):
    """Return a configured oslo_messaging notifier."""
    notifier = oslo_messaging.Notifier(transport, serializer=_SERIALIZER)
    return notifier.prepare(publisher_id=publisher_id)
