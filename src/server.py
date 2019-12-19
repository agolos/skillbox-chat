#  Created by Alexandr Golosseyev
#
#  Copyright © 2019
#
#  Сервер для обработки сообщений от клиентов
#
from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver
import datetime


class ServerProtocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None

    def connectionMade(self):
        self.factory.clients.append(self)

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)

    def send_history(self):
        """Return last 10 chat message."""
        counter = 10
        self.factory.history = self.factory.history[-10:]
        for hist_rec in self.factory.history:
            self.sendLine(f"{hist_rec}".encode())
            counter -= 1
            if counter == 0:
                break

    def lineReceived(self, line: bytes):
        try:
            content = line.decode()
            if self.login is not None:
                cur_time = datetime.datetime.today()
                content = f"{cur_time:%Y-%m-%d %H:%M:%S} : Message from {self.login}: {content}"
                self.factory.history.append(content)
                for user in self.factory.clients:
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
                        self.sendLine(f"Login {new_login} is already exist, try another".encode())
                        self.transport.loseConnection()
                else:
                    self.sendLine("Invalid login!".encode())
        except UnicodeDecodeError:
            print("Decode Error")
        except:
            print("Unknown issue")


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
