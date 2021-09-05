from BankDBM import BankDBM
import json
import socket

from BankDBM import BankDBM

class Server:
    TransactionManager = BankDBM()

    def __init__(self):

        # self.load_data()
        pass

    
    def create_client(self,serverSock):                                     #<---------- Creates a new client ---------->
        data = ""
        data = serverSock.recv(1024).decode()                               #Receives the data of the new client/account to create.
        data = json.loads(data)                                             #Transforms data into json hashMap format.
        
        transactionResult = self.TransactionManager.create_account(data)    #Calls Database Manager with the data for account registration.
        
        serverSock.send(transactionResult.encode())                         #Sends back to client the transaction result.
    
    def verify_user(self, serverSock):                                      #<---------- Verifies if the user exists ---------->
        data = ""
        data = serverSock.recv(1024).decode()                               #Receives the data of the new client/account to verify.
        result = self.TransactionManager.verify_account(data)               #Calls Database Manager with the data for verifying if the account exists.
        result = str(result)                                                #Transforms into string the result returned by the Database manager.

        serverSock.send(result.encode())                                    #Sends back to client the transaction result.

    def verify_password(self,serverSock):                                   #<---------- Verifies if the password is correct for a selected account ---------->
        data = ""
        data = serverSock.recv(1024).decode()                               #Receives the data of the new client/account to verify.
        data = json.loads(data)                                             #Transforms data into json hashMap format.

        result = self.TransactionManager.verify_password(data)              #Calls Database Manager with the data for verifying if the password is correct.
        result = str(result)                                                #Transforms into string the result returned by the Database manager.

        serverSock.send(result.encode())                                    #Sends back to client the transaction result.
    
    def get_user_data(self,serverSock):                                     #<---------- Gets user data corresponding to the account ID received ---------->
        data = ""
        data = serverSock.recv(1024).decode()                               #Receives the data of the new client/account to verify.
        
        result = self.TransactionManager.get_user_data(data)                #Calls Database Manager with the ID for retreiving all the data matching that ID.

        result = json.dumps(result)                                         #Transforms the json hashMap into json string format.

        serverSock.send(result.encode())                                    #Sends data back to client.

    def make_deposit(self,serverSock):                                      #<---------- Makes a deposit to the sent account ID ---------->
        data = ""
        data = serverSock.recv(1024).decode()                               #Receives the data of the new client/account to verify.
        data = json.loads(data)                                             #Transforms data into json hashMap format.

        self.TransactionManager.make_deposit(data)                          #Calls Database Manager with the needed data for making a deposit (Sender, Receptor, Amount).

        result = "Success"                                                  #Defines transaction result.

        serverSock.send(result.encode())                                    #Sends transaction result back to client.

    def initialize_server(self):                                            #<---------- Initializes server ---------->
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)          #Prepares the socket connection.
        server.bind(("127.0.0.1",5010))                                     #Binds the socket to an IP and port.
        server.listen(5)                                                    #Specifies the number of unaccepted connections that the system will allow before refusing new connections.
        print("Server listening for requests")
        while(True):                                                        #Main server loop.
            serverSock, clienteAddr = server.accept()                       #The main socket starts listening for requests.
            
            transaction=""                      
            transaction = serverSock.recv(1024).decode()                    #Awaits for requests.
            # print("Transaction: "+str(transaction))
                                                                            #<---------- Starts the function calling process depending of each received transaction ---------->
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

                                                                            #<---------- Ends the function calling process depending of each received transaction ---------->
            serverSock.close()
            #server.close()


if __name__ == "__main__":      #What is going to be executed when the client runs.
    S = Server()                #Creates an object from the 'Server' class.
    # S.load_data()
    S.initialize_server()       #Initializes client.
