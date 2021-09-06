import json
# from hashlib import sha256


class BankDBM:
    def __init__(self):
        self.accounts = ""
        # self.balances = ""
        self.load_data()

    

    def create_account(self,data):                                          #<---------- Process for creating an account in the database ---------->

        profile = data                                                      #Defines the data as profile.
        self.accounts[profile["ID"]] = {"Name": profile["Name"],            #Creates registry into the hashmap that contains all users data.
                                        "Age": profile["Age"], 
                                        "Sex": profile["Sex"],
                                        "Password": profile["Password"],
                                        "Balance": 0 }
        self.save_file(self.accounts)                                       #Saves the new database into the file.

        return "Success"

    def get_user_data(self,userID):                                         #<---------- Returns a specified user data ---------->

        return self.accounts[userID]

    def verify_account(self,data):                                          #<---------- Validates and returns if a user exists ---------->
        return data in self.accounts

    def verify_password(self,data):                                         #<---------- Validates if the received password and user, matches the access credentials for a registered user ---------->
        profile = data

        if profile["ID"] in self.accounts:
            return self.accounts[profile["ID"]]["Password"] == profile["Password"]
        else: 
            return False

    def make_deposit(self,data):                                            #<---------- Manages balances of the 2 accounts that are involved in a deposit transaction ---------->
        senderID = data["Sender"]
        receptorID = data["Receptor"]
        amount = data["Amount"]

        self.accounts[senderID]["Balance"] -= amount
        self.accounts[receptorID]["Balance"] += amount

        self.save_file(self.accounts)

        
    def save_file(self, data):                                              #<---------- Saves the current hashmap with accounts data and dumps it into a json file ---------->
        with open('accounts.json',"w") as file:
            
            json.dump(data, file)
        # self.load_data()

    def load_data(self):                                                    #<---------- Loads all the data from the json database file ---------->
        with open("accounts.json",) as file:

            data = json.load(file)
            self.accounts = { profile: {"Name": data[profile]["Name"], "Age": data[profile]["Age"], "Sex": data[profile]["Sex"], "Password": data[profile]["Password"], "Balance": data[profile]["Balance"]} for profile in data}
            # self.balances = { profile: data[profile]["Balance"] for profile in data}
            # print(self.accounts)
