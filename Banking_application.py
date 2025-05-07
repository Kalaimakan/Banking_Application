import os
from datetime import datetime
from tabulate import tabulate
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

# ----read_file(Admin_File)

def write_file(filename,data):
    with open(filename,"a") as f:
        f.write(f"{data}\n")


def overwrite_file(filename,lines):
    with open(filename,"w") as f:
        f.write('\n'.join(lines)+'\n')
        
# ----Auto generate Account Numbers
def generate_account_number():
    Start_Account_number = 10001
    for line in read_file(Account_File):
        parts = line.split("|")
        if parts[0].isdigit():
            Start_Account_number = int(parts[0]) + 1
    return Start_Account_number
generate_account_number()
# ----Auto generate customer Id.
def generate_customer_Id():
    start_customer_id=1001
    for line in read_file(Customer_File):
        parts=line.split("|")
        if parts[0].isdigit():
            start_customer_id=int(parts[0])+1
    return start_customer_id     
generate_customer_Id()


# ----Password Verification
def verify_password():
    while True:
        customer_accountNo=input("Enter Your Account Number : ")
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

# ----Customer login
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
# ----Customer Creation.
def create_customer():
    customer_name = input("Enter Customer Name : ")
    while True:
        customer_id = generate_customer_Id()
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

# ----Account Createation.
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


# ----Update customer.
def update_coustomer():
    customer_id=input("Enter your Customer Id To Update : ")
    name_updated=None
    updated_line=[]
    for line in read_file(Customer_File):
        parts=line.split("|")
        if parts[0]==customer_id:
            new_name=input("Enter your New Name : ")
            new_Password=input("Enter your New Password : ")
            new_email=input("Enter your New Email : ")
            updated_line.append(f"{customer_id}|{new_name}|{new_email}|{new_Password}")
            name_updated=new_name
            print([customer_id , new_name , new_email , new_Password])
        else:
            updated_line.append(line)

    if name_updated:
        overwrite_file(Customer_File,updated_line)
        print(f"---------Your Details Are Updated {new_name}!--------")
    else:
        print("User Not Found.")
# update_coustomer()

#----Delete Customer.
def delete_customer():
    customer_id=input("Enter the Customer Id : ")
    customer=[]
    account=[]
    for line in read_file(Customer_File):
        customer_na=line.split("|")[1]
        if line.split("|")[0]!=customer_id:
            customer.append(line)
    overwrite_file(Customer_File,customer)

    for line in read_file(Account_File):
        if line.split("|")[1]!=customer_id:
            account.append(line)
    overwrite_file(Account_File,account)
    print(f"--------User {customer_na} and {customer_na}'s Account have been Deleted.--------")
# delete_customer()

#-----View User Details
def view_user_details():
    # print("--------All Customers.--------")
    # print(f"{'Customer ID':<15}{'Name':<15}{'Email':<23}{'Password':<20}")
    # print("-" * 85)
    # for line in read_file(Customer_File):
    #     customer_id, name, email, password = line.strip().split("|")
    #     print(f"{customer_id:<15}{name:<15}{email:<23}{password:<20}")

    print("--------All Customers.--------")
    data=[]
    for line in read_file(Customer_File):
        parts= line.strip().split("|")
        data.append(parts)

    headers=["Customer ID", "Name", "Email", "Password"]
    print(tabulate(data, headers=headers, tablefmt="fancy_grid",colalign=("left", "left", "left", "left")))
view_user_details()


#-------------Commen Function.--------------
# ----Deposit Function.
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
                write_file(Transaction_File,f"{datetime.now()}| Deposit |{customer_id}|{customer_accountNo}|{deposit_amount}")
            else:
                updated_line.append(line.strip())
        overwrite_file(Account_File,updated_line)
        print(f"--------Deposit Amount Rs.{deposit_amount}.00 Successfully added your Account.---------")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        
# deposit_money()
# print(read_file(Account_File))

# ----withdraw function.
def withdraw_money():
    try:
        customer_accountNo, customer_id = verify_password()

        updated_lines = [] 
        for line in read_file(Account_File):
            customer_account, customer_Id, customer_balance = line.strip().split("|")
            if customer_accountNo == customer_account and customer_id == customer_Id:
                while True :
                    try:
                        withdraw_amount = float(input("Enter your Withdraw Amount: "))
                        if withdraw_amount <= 0:
                            print("Invalid Amount. Please enter a positive number.")
                            continue 
                        if withdraw_amount > float(customer_balance):
                            print("-----Insufficient funds 😞-----")
                            continue
                        new_balance = float(customer_balance) - withdraw_amount
                        print(f"-----Withdrawal successful. Your new balance is Rs.{new_balance}.00-----")
                        updated_lines.append(f"{customer_accountNo}|{customer_id}|{new_balance}")
                        write_file(Transaction_File, f"{datetime.now()}| Withdraw |{customer_id}|{customer_accountNo}|{withdraw_amount}")
                        break
                    except ValueError:
                        print("Invalid amount. Please enter a valid number.") 
            else:
                updated_lines.append(line.strip())

        overwrite_file(Account_File, updated_lines)
        print(f"--------Withdraw Amount Rs.{withdraw_amount} Successfully Withdrawn from your Account.--------")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
# withdraw_money()

# ----View My Transaction History
def view_transaction():
    customer_accountNo,customer_id=verify_password()
    print("--------Your Transaction History.--------")
    for line in read_file(Transaction_File):
        if customer_id in line:
            print(line)
# view_transaction()

#-------------Menus.--------------

# Admin Menu
def admin_menu():
    print("--------------Admin Menu---------------")
    while True:
        print("--------What do you want to do?---------")
        print("01.User Creation.")
        print("02.Account Creation.")
        print("03.Deposit Money.")
        print("04.Withdraw Money.")
        print("05.view Transactions.")
        print("06.Update User.")
        print("07.Delete User.")
        print("08.View User Details.")        
        print("09.Exit.")
        choose_option=int(input("Enter the option (The number must be positive and 1 to 9) :")) 
        if choose_option==1:
            print("--------You can Create New User Now 😊.--------")
            create_customer()
        elif choose_option==2:
            print("--------You can Create Your Account Now 😊.--------")
            account_create()
        elif choose_option==3:
            print("You can Deposit the Money now")
            deposit_money()
        elif choose_option==4:
            print("You can Withdraw the Money now")
            withdraw_money()
        elif choose_option==5:
            print("You Can View Transaction.")
            view_transaction()
        elif choose_option==6:
            print("You can Update a User Now.")
            update_coustomer()
        elif choose_option==7:
            print("You can Delete a User Now.")
            delete_customer()
        elif choose_option==8:
            view_user_details()
        elif choose_option==9:
            print("Thank you")
            commen_menu()
        else:
            print("I already told you. You must Enter the positive number and between 1 to 9 😡")
       
# Customer Menu
def customer_menu():
    while True:
        if customer_name:
            print(f'------------Welcome to our Bank Mr/Mrs.{customer_name}!😊------------')
        else:
            print("------------ Welcome to the Bank! ------------")

        print("01.Deposit Money.")
        print("02.Withdraw Money.")
        print("03.Check Balance.")
        print("04.Transaction History.")
        print("05.Exit.")

        choose_option=int(input("Enter the option (The number must be positive and 1 to 6) :")) 

        if choose_option==1:
            deposit_money()
        elif choose_option==2:
            withdraw_money()
        elif choose_option==3:
            print(f'Your Current Balance is Rs.{Account_balance}.00')
        elif choose_option==4:
            print('i will do it in 3 or 4 Days.🤣🤣')
        elif choose_option==5:
            print(f'Thank you for Choosing Our Bank {user_name}🫡')
            exit()
        else:
            print("I already told you. You must Enter the positive number and between 1 to 6 😡")


# commen menue
def commen_menu():
    print("----------Welcome to our Mini Banking System----------")
    print("01.Admin Login")
    print("02.Customer Login")
    print("03.Exit")
    choose=int(input("Choose Your Choise (between 1 to 3) :"))
    if choose==1 and admin_login():
        admin_menu()
        return
    elif choose==2 and customer_login():
        print("hi")
        # customer_menu()
    elif choose==3:
        print("-----Thankyou for Using our Bank 🫡.------")
        exit()
    else:
        print("-----I already Told you to choose the number between 1 to 3 🤬-----")

commen_menu()