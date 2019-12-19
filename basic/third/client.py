#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Пример клиента на Twisted
#
from twisted.internet import reactor
from twisted.internet.protocol import ClientFactory
from twisted.protocols.basic import LineOnlyReceiver



class ConnectorProtocol(LineOnlyReceiver):
    factory: 'Connector'

    def connectionMade(self):
        #login:admin
        self.sendLine("login:admin".encode())

    def lineReceived(self, line): #call connection
        print(line)


class Connector(ClientFactory):
    protocol = ConnectorProtocol

reactor.connectTCP("localhost", 1234, Connector())
reactor.run()