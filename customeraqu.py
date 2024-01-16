import requests


class CustomerAqu():
    def __init__(self):
        self.first_name = ""
        self.last_name = ""
        self.email = ""
        self.inquiry()

    def inquiry(self):
        registred = input("Have you registered already? Type yes or no\n").lower()
        if registred == "no":
            self.first_name = input("What is your first name?\n")
            self.last_name = input("What is your last name?\n")
            self.email = input("What is your email?\n")
            email_ver = input("Type your email again\n")
            flag = True
            while flag:
                if email_ver == self.email:
                    print("Success you've been added to the newsletter!")
                    body = {
                        "user": {
                            "firstName": self.first_name,
                            "lastName": self.last_name,
                            "email": self.email
                        }
                    }
                    SHEET_USERS = "https://api.sheety.co/1736d1a344c9fc7c65bf9da232fb44b6/flightDeals/users"
                    response = requests.post(url=SHEET_USERS, json=body)
                    response.raise_for_status()
                    flag = False
                else:
                    print("emails do not match")
                    self.email = input("What is your email?\n")
                    email_ver = input("Type your email again\n")
        else:
            print("okay!")

    def list_of_emails(self):
        SHEET_USERS = "https://api.sheety.co/1736d1a344c9fc7c65bf9da232fb44b6/flightDeals/users"
        body = {
            "user": {
                "firstName": self.first_name,
                "lastName": self.last_name,
                "email": self.email
            }
        }

        response = requests.get(url=SHEET_USERS, json=body)
        data = response.json()["users"]
        emails = [data[n]["email"] for n in range(len(data))]
        return emails
