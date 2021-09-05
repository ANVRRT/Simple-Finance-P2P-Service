import json
# from hashlib import sha256


class BankDBM:
    def __init__(self):
        self.accounts = ""
        # self.balances = ""
        self.load_data()
        pass

    

    def create_account(self,data):

        profile = data
        self.accounts[profile["ID"]] = {"Name": profile["Name"], 
                                        "Age": profile["Age"], 
                                        "Sex": profile["Sex"],
                                        "Password": profile["Password"],
                                        "Balance": 0 }
        self.save_file(self.accounts)

        return "Success"

    def get_user_data(self,userID):

        return self.accounts[userID]

    def verify_account(self,data):
        if data in self.accounts:
            return True
        else:
            return False

    def verify_password(self,data):
        profile = data

        if profile["ID"] in self.accounts:
            if self.accounts[profile["ID"]]["Password"] == profile["Password"]:
                return True
            else:
                return False
        else: 
            return False

    def make_deposit(self,data):
        senderID = data["Sender"]
        receptorID = data["Receptor"]
        amount = data["Amount"]

        self.accounts[senderID]["Balance"] -= amount
        self.accounts[receptorID]["Balance"] += amount

        self.save_file(self.accounts)

        
    def save_file(self, data):
        with open('accounts.json',"w") as file:
            
            json.dump(data, file)
        # self.load_data()

    def load_data(self):
        with open("accounts.json",) as file:

            data = json.load(file)
            self.accounts = { profile: {"Name": data[profile]["Name"], "Age": data[profile]["Age"], "Sex": data[profile]["Sex"], "Password": data[profile]["Password"], "Balance": data[profile]["Balance"]} for profile in data}
            # self.balances = { profile: data[profile]["Balance"] for profile in data}
            # print(self.accounts)
