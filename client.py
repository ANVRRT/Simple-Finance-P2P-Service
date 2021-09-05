from hashlib import sha256
import socket
import json
import time
from input_manager import InputManager

class Client:
    def __init__(self):
        self.sessionID = ""
        self.sessionName = ""
        self.sessionAge = ""
        self.sessionSex = ""
        self.sessionPassword = ""
        self.sessionBalance = 0
        self.sessionData = {}
    
    def start_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("127.0.0.1",5010))
    
    def stop_socket(self):

        self.sock.close()
    
    def process_data(self):
        
        while True:
            self.start_socket()
            profileID = InputManager.define_string("Please enter your new account ID")
            
            transactionType = "verifyUser"
            self.sock.send(transactionType.encode())

            time.sleep(1)
            self.sock.send(profileID.encode())
            transactionResult = self.sock.recv(1024).decode()
            # print(transactionResult)
            self.stop_socket()
            if transactionResult == "True":
                InputManager.display_message("This account ID is already registered, please try another one")
            else:
                break

        profileName = InputManager.define_string("Please enter your full name:")
        profileAge = InputManager.define_numbers(message="Please enter your age (Must be greater or equal than 18):", infLimit = 18,typeOfNumber = int)
        profileSex = InputManager.define_string("Please enter the letter corresponding to your sex (Male = M) (Female = F):")
        profilePassword = sha256(InputManager.define_string(message="Please enter your password, must be minimum 6 characters long, maximum 30:", infLimit=6, supLimit=30).encode())

        profileData = {"ID": profileID, "Name": profileName, "Age": profileAge, "Sex": profileSex, "Password": profilePassword.hexdigest()}
        # print(self.profileData)
        return profileData
        

    def create_account(self):

        
        
        profileData = self.process_data()

        self.start_socket()
        
        transactionType = "createClient"
        self.sock.send(transactionType.encode())

        data = json.dumps(profileData)

        time.sleep(1)
        self.sock.send(data.encode())

        transactionResult = self.sock.recv(1024).decode()

        self.stop_socket()
        InputManager.display_message("Transaction result: " + transactionResult)

    def log_in(self):

        sessionID = InputManager.define_string("Please enter your new account ID")


        self.start_socket()
        sessionPassword = sha256(InputManager.define_string(message="Please enter your password:", infLimit=6, supLimit=30).encode()).hexdigest()
        
        transactionType = "verifyPassword"
        self.sock.send(transactionType.encode())

        profileData = {"ID": sessionID, "Password": sessionPassword }
        data = json.dumps(profileData)
        self.sock.send(data.encode())

        transactionResult = self.sock.recv(1024).decode()

        self.stop_socket()
        # print(transactionResult)
        if transactionResult == "False":
            InputManager.display_message("The password for this account is incorrect, please try again")
            return False
        else:
            self.sessionID = sessionID
            self.sessionPassword = sessionPassword
            return True

    def get_user_data(self):
        self.start_socket()

        transactionType = "getUserData"
        self.sock.send(transactionType.encode())

        time.sleep(1)
        self.sock.send(self.sessionID.encode())

        transactionResult = self.sock.recv(1024).decode()
        self.stop_socket()
        self.sessionData = json.loads(transactionResult)

        self.sessionName = self.sessionData["Name"]
        self.sessionAge = self.sessionData["Age"]
        self.sessionSex = self.sessionData["Sex"]
        self.sessionBalance = self.sessionData["Balance"]


    def main_menu(self):
        def display_balance():
            InputManager.display_message(message=f"Your current balance is: {self.sessionBalance}")

        def display_account_data():
            print("")
            print(f"Your registered ID is   : {self.sessionID}")
            print(f"Your registered Name is : {self.sessionName}")
            print(f"Your registered Age is  : {self.sessionAge}")
            print(f"Your registered Sex is  : {self.sessionSex}")
            print(f"Your current Balance is : {self.sessionBalance}")
            InputManager.display_message(message="")

        def validate_balance(amount):
            if amount > self.sessionBalance:
                return False
            else:
                return True

        def send_payment():
            
            self.start_socket()
            receptorID = InputManager.define_string("Please enter the receptor ID:")
            
            transactionType = "verifyUser"
            self.sock.send(transactionType.encode())

            time.sleep(1)
            self.sock.send(receptorID.encode())
            transactionResult = self.sock.recv(1024).decode()
            # print(transactionResult)
            self.stop_socket()
            if transactionResult == "False":
                InputManager.display_message(f"This account ID '{receptorID}' doesn't exists")
                return

            print(f"You currently have ${self.sessionBalance}")
            sendingAmount = InputManager.define_numbers(message="Enter the amount you want to send:", infLimit = 1, typeOfNumber = float)
            approvalFlag = validate_balance(sendingAmount)
            if not approvalFlag:
                InputManager.display_message("You dont have enough money")
                return
            
            data = {"Sender": self.sessionID, "Receptor": receptorID, "Amount": sendingAmount}
            data = json.dumps(data)

            self.start_socket()

            transactionType = "makeDeposit"
            self.sock.send(transactionType.encode())

            time.sleep(1)
            self.sock.send(data.encode())

            transactionResult = self.sock.recv(1024).decode()

            self.stop_socket()
            
            self.sessionBalance -= sendingAmount

            InputManager.display_message(f"Transaction result: {transactionResult}")








        self.get_user_data()
        while True:
            print("")
            print("*****************************************************")
            print(f"WELCOME {self.sessionID}")
            print("")
            print("1) See current balance")
            print("2) Send payment")
            print("3) See my account data")
            print("4) Exit")
            print("")
            print("*****************************************************")
            selectedOption = InputManager.define_numbers(message="Type a number according to your selected option:", infLimit = 1, supLimit = 4,typeOfNumber = int)
            if selectedOption == 4:
                break
            
            if selectedOption == 1:
                display_balance()
            
            if selectedOption == 2:
                send_payment()

            if selectedOption == 3:
                display_account_data()



    def initialize_client(self):

        while True:
            print("")
            print("*****************************************************")
            print("WELCOME TO THE PYTHON BANK P2P SERVICE")
            print("")
            print("1) Log in")
            print("2) Create account")
            print("3) Exit")
            print("")
            print("*****************************************************")
            selectedOption = InputManager.define_numbers(message="Type a number according to your selected option", infLimit = 1, supLimit = 3,typeOfNumber = int)
            if selectedOption == 3:
                print()
                print("THANKS FOR USING THE PYTHON BANK P2P SERVICE")
                print()
                break
            if selectedOption == 1:
                logFlag = self.log_in()
                if logFlag:
                    self.main_menu()
                pass

            if selectedOption == 2:
                self.create_account()

            if selectedOption == 3:
                pass

            
    



if __name__ == "__main__":
    client = Client()
    client.initialize_client()