from pathlib import Path
import json
import random
import string
class Bank:
    DataBase = 'DataBase.json'
    data = []

    try:
        if Path(DataBase).exists():
            with open(DataBase) as fs:
                data = json.loads(fs.read())
        else:
            print("Sorry, we are facing some issues.")                                              

    except Exception as err:
        print(f"An error occured as {err}.")

    @classmethod
    def __update(cls):
        with open(cls.DataBase, 'w') as fs:
            fs.write(json.dumps(cls.data))
    @staticmethod
    def __accountno():
        alpha = random.choices(string.ascii_letters, k = 5)
        digits = random.choices(string.digits, k = 4)
        id = alpha + digits
        random.shuffle(id)
        return "".join(id) #["".join is used to convert list into string]

    def create_account(self):
        d = {
            "Name": input("Please enter your name: "),
            "Email": input("Please enter your email: "),
            "Phone No.": input("Please enter your phone number: "),
            "Pin": int(input("Pease enter your pin (4 digits)")),
            "Account No.": Bank.__accountno(),
            "Balance": 0
            }
        print(f"please note down account number :{d['Account No.']}")

        if len(str(d["Pin"])) != 4:
            print(f"Please review your pin.")

        elif len(str(d["Phone No."])) != 10:
            print("Please review your phone no.")
        
        else:
            Bank.data.append(d)
            Bank.__update()

    def deposite_money(self):
        AccNo = input("Please enter your account number: ")
        Pin = int(input("Enter your pin: "))
        user_data = [i for i in Bank.data if i['Account No.'] == AccNo and i['Pin'] == Pin]
        
        if not user_data:
            print("User not found.")
        else:
            amount = int(input("Enter amount to be deposited: "))
            if amount <= 0:
                print("Invalid amount.")
            elif amount > 10000:
                print("Amount greater than 10000")
            else:
                user_data[0]['Balance'] += amount
                Bank.__update()
                print("Amount credited.")

    def withdraw_money(self):
        AccNo = input("Please enter your account number: ")
        Pin = int(input("Enter your pin: "))
        user_data = [i for i in Bank.data if i['Account No.'] == AccNo and i['Pin'] == Pin]
        
        if not user_data:
            print("User not found.")
        else:
            amount = int(input("Enter amount to be withdrw: "))
            if amount <= 0:
                print("Invalid amount.")
            elif amount > 10000:
                print("Amount greater than 10000")
            else:

                if user_data[0]['Balance'] < amount:
                    print("Insufficient Balance")
                else:
                    user_data[0]['Balance'] -= amount
                    Bank.__update()
                    print("Amount debited.")

    def details(self):
        AccNo = input("Please enter your account number: ")
        Pin = int(input("Enter your pin: "))
        user_data = [i for i in Bank.data if i['Account No.'] == AccNo and i['Pin'] == Pin]
        
        if not user_data:
            print("User not found.")
        else:
            for i in user_data[0]:
                if i == "Pin": #[To not show pin]
                    continue
                else:
                    print(f"{i}: {user_data[0][i]}")

    def update_details(self):
        AccNo = input("Please enter your account number: ")
        Pin = int(input("Enter your pin: "))
        user_data = [i for i in Bank.data if i['Account No.'] == AccNo and i['Pin'] == Pin]
        if not user_data:
            print("User not found.")
        else:
            print("You cannot change account number.")
            print("Now you can update your details and skip it if you don't want to update.")
            new_data = {
                "Name": input("Enter your new name: "),
                "Email": input("Enter your new email: "),
                "Phone No.": input("Enter your new phone number: "),
                "Pin": input("Enter your new pin: ")
            }
            for i in new_data:
                if new_data[i] == "":
                    new_data[i]= user_data[0][i]
                else:
                    user_data[0][i] = new_data[i]
            print(new_data)
            new_data["Account No."] = user_data[0]["Account No."]
            new_data["Balance"] = user_data[0]["Balance"]

            for i in user_data[0]:
                if user_data[0][i] == new_data[i]:
                    continue
                else:
                    if new_data[i].isnumeric():
                        user_data[0][i] = int(new_data[i])
                    else:
                        user_data[0][i] = new_data[i]
            print("user_data")
            Bank.__update()
            print("Data Updated...")

    def delete_account(self):
        AccNo = input("Please enter your account number: ")
        pin =int(input("Enter your pin: "))
        for i in Bank.data:
            if i["Account No."] == AccNo and i["Pin"] == pin:
                Bank.data.remove(i)
            else:
                print("user not found")   
        Bank.__update()
        print("Account Deleted...")


user = Bank()
print("Press 1 for creating an account.")
print("Press 2 to deposit money.")
print("Press 3 to withdraw money.")
print("Press 4 for details.")
print("Press 5 for updating the details.")
print("Press 6 for deleting the account.")

check = int(input("Enter your choice :- "))

if check == 1:
    user.create_account()

if check == 2:
    user.deposite_money()

if check == 3:
    user.withdraw_money()

if check == 4:
    user.details()

if check == 5:
    user.update_details()

if check == 6:
    user.delete_account()