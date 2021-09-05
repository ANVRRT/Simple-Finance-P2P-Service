from BankDBM import BankDBM
import json
import socket

from BankDBM import BankDBM

class Server:
    TransactionManager = BankDBM()

    def __init__(self):

        # self.load_data()
        pass

    
    def create_client(self,serverSock):
        data = ""
        data = serverSock.recv(1024).decode()
        data = json.loads(data)
        
        transactionResult = self.TransactionManager.create_account(data) #CHANGE INTO BANKDBC
        
        serverSock.send(transactionResult.encode())
        print("Sent Message: "+str(transactionResult))
    
    def verify_user(self, serverSock):
        data = ""
        data = serverSock.recv(1024).decode()
        result = self.TransactionManager.verify_account(data)
        result = str(result)

        serverSock.send(result.encode())

    def verify_password(self,serverSock):
        data = ""
        data = serverSock.recv(1024).decode()
        data = json.loads(data)

        result = self.TransactionManager.verify_password(data)
        result = str(result)

        serverSock.send(result.encode())
    
    def get_user_data(self,serverSock):
        data = ""
        data = serverSock.recv(1024).decode()
        
        result = self.TransactionManager.get_user_data(data)

        result = json.dumps(result)

        serverSock.send(result.encode())

    def make_deposit(self,serverSock):
        data = ""
        data = serverSock.recv(1024).decode()
        data = json.loads(data)

        self.TransactionManager.make_deposit(data)

        result = "Success"

        serverSock.send(result.encode())

    def initialize_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1",5010))
        server.listen(5)
        print("Server listening for requests")
        while(True):            
            serverSock, clienteAddr = server.accept()
            
            transaction=""
            transaction = serverSock.recv(1024).decode()
            # print("Transaction: "+str(transaction))
            
            # transaction Capturar datos
            if(transaction == "createClient"):

                self.create_client(serverSock)

            if (transaction == "verifyUser"):

                self.verify_user(serverSock)

            if (transaction == "verifyPassword"):

                self.verify_password(serverSock)

            if (transaction == "getUserData"):

                self.get_user_data(serverSock)

            if (transaction == "makeDeposit"):
                
                self.make_deposit(serverSock)


            serverSock.close()
            #server.close()


if __name__ == "__main__":
    S = Server()
    # S.load_data()
    S.initialize_server()
