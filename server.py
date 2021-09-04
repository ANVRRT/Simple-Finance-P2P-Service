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
        data=""
        data = serverSock.recv(1024).decode()
        print(data)
        data = json.loads(data)
        
        result=""
        result = self.TransactionManager.create_account(data) #CHANGE INTO BANKDBC
        
        transactionResult = result + "\n"
        serverSock.send(transactionResult.encode())
        print("Sent Message: "+str(transactionResult))
    
    def verify_user(self, serverSock):
        pass

    # def load_data(self):
    #     file = open("jsonFile.json",)

    #     data = json.load(file)
    #     self.accounts = { profile: {"Name": data[profile]["Name"], "Age": data[profile]["Age"], "Sex": data[profile]["Sex"]} for profile in data}
    #     self.balances = { profile: data[profile]["Balance"] for profile in data}
    #     print(self.accounts)

    def initialize_server(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(("127.0.0.1",5010))
        server.listen(5)

        # Use server debe estar en un cliclo atendiendo a clientes
        while(True):
            print("Estado Listen...\nEsperando peticiones de conexion... \n")
            
            serverSock, clienteAddr = server.accept()
            
            # 1. Obtener transaction a realizar
            transaction=""
            transaction = serverSock.recv(1024).decode()
            print("Transaction: "+str(transaction))
            
            # transaction Capturar datos
            if(transaction == "createClient\n"):

                self.create_client(serverSock)
                # data=""
                # data = serverSock.recv(1024).decode()
                # print(data)
                # data = json.loads(data)
                
                # result=""
                # result = self.TransactionManager.create_account(data) #CHANGE INTO BANKDBC
                
                # transactionResult = result + "\n"
                # serverSock.send(transactionResult.encode())
                # print("Sent Message: "+str(transactionResult))
            
            if (transaction == "verifyUser\n"):
                self.verify_user(serverSock)

            
            serverSock.close()
            #server.close()


if __name__ == "__main__":
    S = Server()
    # S.load_data()
    S.initialize_server()
