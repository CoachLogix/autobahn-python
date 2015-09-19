from autobahn.twisted.wamp.connection import Connection


def on_join(session):
    """
    This is user code triggered when a session was created on top of
    a connection, and the sessin has joined a realm.
    """
    print('session connected: {}'.format(session))

    def on_leave(details):
        print("on_leave", details)

    session.on_leave(on_leave)

    # explicitly leaving a realm will disconnect the connection
    # cleanly and not try to reconnect, but exit cleanly.
    session.leave()


def main(connection):
    """
    This is the main entry into user code. It _gets_ a connection
    instance, which it then can hook onto.
    """
    def on_connect(session):
        session.on_join(on_join)
        session.join(u'public')

    # we attach our listener code on the connection. whenever there
    # is a session created which has joined, our callback code is run
    connection.on_connect(on_connect)


if __name__ == '__main__':

    from twisted.internet.task import react

    # multiple, configurable transports, either via dict-like config, or
    # from native Twisted endpoints
    transports = [
        {
            "type": "websocket",
            "url": "ws://127.0.0.1:8080/ws"
        }
    ]

    # a connection connects and automatically reconnects WAMP client
    # transports to a WAMP router. A connection has a listener system
    # where user code can hook into different events : on_join
    connection = Connection(transports=transports, realm=u'public', extra=None)

    # the following returns a deferred that fires when the connection is
    # finally done: either by explicit close by user code, or by error or
    # when stop reconnecting
    react(connection.connect, (main,))
