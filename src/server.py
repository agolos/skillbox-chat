#  Created by Artem Manchenkov
#  artyom@manchenkoff.me
#
#  Copyright © 2019
#
#  Сервер для обработки сообщений от клиентов
#
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver


class ServerProtocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None

    def connectionMade(self):
        self.factory.clients.append(self)

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)

    def send_history(self):
        counter = 10
        for i in range(len(self.factory.history) - 10, len(self.factory.history)):
            self.sendLine(f"{self.factory.history[i]}".encode())
            counter -= 1
            if counter == 0:
                break

    def lineReceived(self, line: bytes):
        try:
            content = line.decode()
            if self.login is not None:
                content = f"Message from {self.login}: {content}"
                self.factory.history.append(content)
                for user in self.factory.clients:
                    if user is not self:
                        user.sendLine(content.encode())
            else:
                # login:admin -> admin

                if content.startswith("login:"):
                    is_new_login = True
                    new_login = content.replace("login:", "")
                    for user in self.factory.clients:
                        if user.login == new_login:
                            is_new_login = False
                            break
                    if is_new_login:
                        self.login = new_login
                        self.sendLine("Welcome!".encode())
                        self.send_history()
                    else:
                        self.sendLine(f"Логин {new_login} занят, попробуйте другой".encode())
                else:
                    self.sendLine("Invalide login!".encode())
        except:
            print("Decode Error")



class Server(ServerFactory):
    protocol = ServerProtocol
    clients = list()
    history = list()

    def stopFactory(self):
        print("Server was closed")

    def startFactory(self):
        print("Server started")



reactor.listenTCP(1234, Server())
reactor.run()