from hashlib import sha256
import socket
import json
from input_manager import InputManager

class Client:
    def __init__(self):
        self.sesionID = ""
        self.sesionName = ""
        self.sesionAge = ""
        self.sesionSex = ""
        self.sesionPassword = ""
        self.sesionData = {}
    
    def start_socket(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("127.0.0.1",5010))
    
    def stop_socket(self):

        self.sock.close()
    
    def process_data(self):
        profileID = InputManager.define_string("Please enter your new account ID")
        
        #VERIFY THAT THE ID DOESN'T EXISTS

        profileName = InputManager.define_string("Please enter your full name")
        profileAge = InputManager.define_numbers(message="Please enter your age (Must be greater than 18)", infLimit = 18,typeOfNumber = int)
        profileSex = InputManager.define_string("Please enter the letter corresponding to your sex (Male = M) (Female = F)")
        profilePassword = sha256(InputManager.define_string(message="Please enter your password, must be minimum 6 characters long, maximum 30", infLimit=6, supLimit=30).encode())

        profileData = {"ID": profileID, "Name": profileName, "Age": profileAge, "Sex": profileSex, "Password": profilePassword.hexdigest()}
        # print(self.profileData)
        return profileData
        

    def create_account(self):

        profileData = self.process_data()
        self.start_socket()
        
        transactionType = "createClient\n"
        data = json.dumps(profileData)

        self.sock.send(transactionType.encode())
        self.sock.send(data.encode())

        transactionResult = self.sock.recv(1024).decode()

        self.stop_socket()
        InputManager.display_message("Transaction result: " + transactionResult)

    def log_in(self):

        self.sesionID = InputManager.define_string("Please enter your new account ID")
        sesionPassword = sha256(InputManager.define_string(message="Please enter your password", infLimit=6, supLimit=30).encode())

        #Call to verify the password

        #NOT FINISHED



        pass

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
                pass

            if selectedOption == 2:
                self.create_account()

            
    



if __name__ == "__main__":
    client = Client()
    client.initialize_client()