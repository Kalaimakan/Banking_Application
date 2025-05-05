import os
from datetime import datetime
max_attempts=3
#-------------File Paths.--------------
Admin_File="admin.txt"
Customer_File="customers.txt"
Account_File="account.txt"
Transaction_File="Transactions.txt"

#-------------initialize files.--------------
def initialize_files():
    if not os.path.exists(Admin_File):
        with open(Admin_File,"w") as f:
            f.write("Admin|Admin1015\n")
    
    for file in [Customer_File,Account_File,Transaction_File]:
        open(file,"a").close()
initialize_files()

#-------------function for read, write and overwrite files--------------
def read_file(filename):
    lines=[]
    with open(filename,"r") as f:
        for line in f:
            line=line.strip()
            if line:
                lines.append(line)
    return lines

# read_file(Admin_File)

def write_file(filename,data):
    with open(filename,"a") as f:
        f.write(f"{data}\n")


def overwrite_file(filename,lines):
    with open(filename,"w") as f:
        f.write('\n'.join(lines)+'\n')
        
# Auto generate Account Numbers
def generate_account_number():
    Start_Account_number = 10000
    for line in read_file(Account_File):
        parts = line.split("|")
        if parts[0].isdigit():
            Start_Account_number = int(parts[0]) + 1
    return Start_Account_number

# Password Verification
def verify_password():
    while True:
        customer_accountNo=input("Enter Your Deposit Account Number : ")
        customer_id=None

        for line in read_file(Account_File):
            if line.split("|")[0]==customer_accountNo:
                customer_id=line.split("|")[1]
                break
        if not customer_id:
             print("-----Account Number Not Found.-----")
             continue
         
        while True:
            customer_password=input("Enter Password to continue : ")
            for line in read_file(Customer_File):
                parts = line.strip().split("|")
                if parts[0]==customer_id and parts[-1]==customer_password:
                    print("-----Login successful-----")
                    return customer_accountNo,customer_id

            print("Incorrect Password. Access Denied.")
# verify_password()

#-------------Login Functions.--------------
# Admin login
def admin_login():
    while True:
        user_name=input("Enter Admin User Name : ")
        password=input("Enter Admin Password : ")

        for line in read_file(Admin_File):
            if line==f"{user_name}|{password}":
                print("Login Successful")
                return True
        print("Incorrect Password. Access Denied.")
# admin_login()

# Customer login
def customer_login():
    attempt=0
    while attempt<max_attempts:
        customer_id=input("Enter Your Id : ")
        Customer_password=input("Enter Your Password : ")
        for line in read_file(Customer_File):
            parts=line.split("|")
            if  parts[0]==customer_id and parts[-1]==Customer_password:
                print("-----Login Successful. You are Good to Go 😊-----")
                return
        attempt+=1
        left_attempts=max_attempts-attempt
        if left_attempts>0:
            print(f"-----You Have Only {left_attempts} Attempts Left 🙁.-----")
        else:
            print("-----Login Failed. Get out of Here 🤬🤬-----")
            print("-----Tooo Many Failed attempts so exiting the program.-----")
            exit()
# customer_login()

#-------------Admin Functions--------------
# Customer Creation.??????????????????????????????????????????????
def create_customer():
    customer_name = input("Enter Customer Name : ")
    while True:
        customer_id = input("Enter Customer User ID (Ex: 1000) : ")
        id_exists=False
        for line in read_file(Customer_File):
            if line.split("|")[0] == customer_id:
                print("-----Customer ID already exists. Try another one.-----")
                id_exists=True
                break
        if not id_exists:
            break
    customer_password = input("Enter Customer Password : ")
    # customer_initial_balance = input("Enter Customer Initial Balance : ")
    customer_email = input("Enter Customer Email Address :")
    data = f"{customer_id}|{customer_name}|{customer_email}|{customer_password}"
    write_file(Customer_File, data)
    print(f"-----{customer_name}'s User Successfully Created 😊.-----")
# create_customer()

# Account Createation???????????????????????????????????????????????????
def account_create():
    # customer_accountNo=input("Enter Customer Account Number : ")
    customer_accountNo=generate_account_number()
    while True:
        customer_id=input("Enter Customer Id : ")
        account_exists=False
        for line in read_file(Customer_File):
            if line.split("|")[0] == customer_id:
                # print("-----Customer Id Not Found.-----")
                account_exists=True
                break
        if not account_exists:
            print("-----Customer ID Not Found. Please create customer first.-----")
            continue
    # cstomer_name = input("Enter Customer Name : ")
        already_has_account = False
        for line in read_file(Account_File):
            if line.split("|")[1] == customer_id:
                print("-----Customer already has an account. Only one account is allowed.-----")
                already_has_account = True
                break
        if already_has_account:
            return  
        else:
            break  # Valid ID and no existing account, proceed
    customer_initial_balance=float(input("Enter Customer Initial Balance :"))
    data=f"{customer_accountNo}|{customer_id}|{customer_initial_balance}"
    write_file(Account_File,data)
    print(f"-----Customer {customer_id}'s Account Successfully Created 😊.-----")
# account_create()



#-------------Commen Function.--------------
# Deposit Function
def deposit_money():
    try:
        customer_accountNo,customer_id=verify_password()
        try:
            deposit_amount=float(input("Enter Your Deposit Amount : "))
            if deposit_amount<0:
                print("Deposit Amount must be grater than 0.")
                return
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            return

        updated_line=[]
        for line in read_file(Account_File):
            customer_account=line.split("|")[0]
            customer_balance=line.split("|")[-1]
            if customer_accountNo==customer_account:
                new_balance=float(customer_balance)+deposit_amount
                updated_line.append(f"{customer_accountNo}|{customer_id}|{new_balance}")
                write_file(Transaction_File,f"{datetime.now()}| Deposit |{deposit_amount}|{customer_accountNo}|{customer_id}")
            else:
                updated_line.append(line.strip())

        overwrite_file(Account_File,updated_line)
        print(f"--------Deposit Amount Rs.{deposit_amount}.00 Successfully added your Account.---------")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
deposit_money()
# print(read_file(Account_File))




#-------------Menus.--------------
# commen menue
# def commen_menu():
#     print("----------Welcome to our Mini Banking System----------")
#     print("01.Admin Login")
#     print("02.Customer Login")
#     print("03.Exit")
#     choose=int(input("Choose Your Choise (between 1 to 3) :"))
#     if choose==1:
#         admin_login()
#     elif choose==2:
#         customer_login()
#     elif choose==3:
#         print("-----Thankyou for Using our Bank 🫡.------")
#         exit()
#     else:
#         print("-----I already Told you to choose the number between 1 to 3 🤬-----")

# commen_menu()

# Main Menu

# def admin_menu():
#     while True:
#         if user_name:
#             print(f'------------Welcome to our Bank Mr/Mrs.{user_name}!😊------------')
#         else:
#             print("------------ Welcome to the Bank! ------------")
#         print("--------What do you want to do?---------")
#         print("01.User Creation.")
#         print("02.Account Creation.")
#         print("03.Deposit Money.")
#         print("04.Withdraw Money.")
#         print("05.view Transactions.")
#         print("06.Update User.")
#         print("07.Delete User.")
#         print("08.View User Details.")        
#         print("09.Exit.")
#         choose_option=int(input("Enter the option (The number must be positive and 1 to 5) :")) 
#         if choose_option==1:
#             print("--------You can Create New User Now 😊.--------")
#             break
#         elif choose_option==2:
#             print("--------You can Create Your Account Now 😊.--------")
#         elif choose_option==3:
#             print("You can Deposit the Money now")
#         elif choose_option==4:
#             print("You can Withdraw the Money now")
#         elif choose_option==5:
#             print("You Can View Transaction.")
#         elif choose_option==6:
#             print("You can Update a User Now.")
#         elif choose_option==7:
#             print("You can Delete a User Now.")
#         elif choose_option==8:
#             print("You can Update the User Now.")
#         elif choose_option==9:
#             print("Thank you")
#             exit()
#         else:
#             print("I already told you. You must Enter the positive number and between 1 to 6 😡")
       


# def customer_menu():
#     while True:
#         if customer_username:
#             print(f'------------Welcome to our Bank Mr/Mrs.{customer_username}!😊------------')
#         else:
#             print("------------ Welcome to the Bank! ------------")

#         print("01.Deposit Money.")
#         print("02.Withdraw Money.")
#         print("03.Check Balance.")
#         print("04.Transaction History.")
#         print("05.Exit.")

#         choose_option=int(input("Enter the option (The number must be positive and 1 to 6) :")) 

#         if choose_option==1:
#             deposit_money()
#         elif choose_option==2:
#             withdraw_money()
#         elif choose_option==3:
#             print(f'Your Current Balance is Rs.{Account_balance}.00')
#         elif choose_option==4:
#             print('i will do it in 3 or 4 Days.🤣🤣')
#         elif choose_option==5:
#             print(f'Thank you for Choosing Our Bank {user_name}🫡')
#             exit()
#         else:
#             print("I already told you. You must Enter the positive number and between 1 to 6 😡")