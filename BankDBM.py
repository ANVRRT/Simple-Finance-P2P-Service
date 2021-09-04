import json
# from hashlib import sha256


class BankDBM:
    def __init__(self):
        self.accounts = ""
        self.balances = ""
        self.load_data()
        pass

    

    def create_account(self,data):

        profile = data
        self.accounts[profile["ID"]] = {"Name": profile["Name"], 
                                        "Age": profile["Age"], 
                                        "Sex": profile["Sex"],
                                        "Password": profile["Password"],
                                        "Balance": 0 }
        self.save__file(self.accounts)

        return "Success"

        
        
    def save__file(self, data):
        with open('accounts.json',"w") as file:
            
            json.dump(data, file)

    def load_data(self):
        with open("accounts.json",) as file:

            data = json.load(file)
            self.accounts = { profile: {"Name": data[profile]["Name"], "Age": data[profile]["Age"], "Sex": data[profile]["Sex"]} for profile in data}
            self.balances = { profile: data[profile]["Balance"] for profile in data}
            print(self.accounts)
