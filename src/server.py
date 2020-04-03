from twisted.internet import reactor
from twisted.internet.protocol import ServerFactory, connectionDone
from twisted.protocols.basic import LineOnlyReceiver


class ConnectorProtocol(LineOnlyReceiver):
    factory: 'Server'
    login: str = None
    login_list: list

    def connectionMade(self):
        self.factory.clients.append(self)

    def connectionLost(self, reason=connectionDone):
        self.factory.clients.remove(self)

    def lineReceived(self, line: bytes):
        content = line.decode()
        #self.login_list = []

        if self.login is not None:
            content = f"Message from {self.login}: {content}"

            for user in self.factory.clients:
                if user is not self:
                    user.sendLine(content.encode())

        else:
            if content.startswith("login:"):
                self.login = content.replace("login:", "")
                if self.login not in self.login_list:
                    self.sendLine("Welcome".encode())
                    self.login_list.append(self.login)
                else:
                    self.sendLine("Login already exists, try another one".encode())
            else:
                self.sendLine("Invalid login".encode())

        # print(f"Message: {line}")


class Server(ServerFactory):
    protocol = ConnectorProtocol
    clients: list

    def startFactory(self):
        self.clients = []
        print('Server started')

    def stopFactory(self):
        print("Server stopped")


reactor.listenTCP(1234, Server())
reactor.run()
