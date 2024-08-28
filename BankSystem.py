import json  # To handle JSON data storage and retrieval
import os  # To interact with the operating system (e.g., file handling)
import random  # To generate random account numbers
from datetime import datetime  # To manage date and time for transactions

# Class representing a bank account
class BankAccount:
    def __init__(self, account_number, account_holder, balance=0.0, transactions=None):
        # Initialize account details
        self.account_number = account_number  # Unique account number
        self.account_holder = account_holder  # Name of the account holder
        self.balance = balance  # Current account balance, default is 0.0
        self.transactions = transactions if transactions is not None else []  # List of transactions, default is an empty list

    # Method to add a transaction to the account's history
    def add_transaction(self, action, amount):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get the current date and time
        transaction_record = {
            "action": action,  # Type of transaction (e.g., Deposit, Withdraw)
            "amount": amount,  # Amount involved in the transaction
            "date_time": timestamp  # Timestamp of the transaction
        }
        self.transactions.append(transaction_record)  # Append the transaction to the transaction history

    # Method to deposit money into the account
    def deposit(self, amount):
        self.balance += amount  # Increase the balance by the deposit amount
        self.add_transaction("Deposit", amount)  # Record the deposit transaction
        print(f"{amount} has been deposited. New balance: {self.balance}")

    # Method to withdraw money from the account
    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds.")  # Check if there are enough funds
        else:
            self.balance -= amount  # Decrease the balance by the withdrawal amount
            self.add_transaction("Withdraw", amount)  # Record the withdrawal transaction
            print(f"{amount} has been withdrawn. New balance: {self.balance}")

    # Method to transfer money to another account
    def transfer(self, target_account, amount):
        if amount > self.balance:
            print("Insufficient funds.")  # Check if there are enough funds
        else:
            self.balance -= amount  # Decrease the balance by the transfer amount
            target_account.balance += amount  # Increase the target account's balance by the transfer amount
            self.add_transaction(f"Transfer to {target_account.account_number}", amount)  # Record the transfer transaction in this account
            target_account.add_transaction(f"Transfer from {self.account_number}", amount)  # Record the transfer transaction in the target account
            print(f"Transferred {amount} to account {target_account.account_number}. New balance: {self.balance}")

    # Method to print a receipt for the last 5 transactions
    def print_receipt(self):
        print("\nTransaction Receipt")
        print("-------------------")
        print(f"Account Holder: {self.account_holder}")
        print(f"Account Number: {self.account_number}")
        print(f"Balance: {self.balance}")
        print("Recent Transactions:")
        for transaction in self.transactions[-5:]:  # Print the last 5 transactions
            print(f"- {transaction['date_time']}: {transaction['action']} {transaction['amount']}")
        print("-------------------\n")

# Class representing the banking system
class BankSystem:
    def __init__(self, data_file='bank_data.json'):
        self.data_file = data_file  # File to store account data
        self.accounts = self.load_accounts()  # Load existing accounts from file

    # Method to load accounts from a JSON file
    def load_accounts(self):
        if os.path.exists(self.data_file):  # Check if the file exists
            with open(self.data_file, 'r') as f:
                try:
                    data = json.load(f)  # Load account data from the file
                    accounts = {acc_num: BankAccount(account_number=acc_num, 
                                                     account_holder=details['account_holder'], 
                                                     balance=details['balance'], 
                                                     transactions=details.get('transactions', [])) 
                                for acc_num, details in data.items()}  # Create BankAccount objects for each account
                    return accounts
                except json.JSONDecodeError:
                    return {}  # Return an empty dictionary if the file is empty or corrupted
        return {}

    # Method to save accounts to a JSON file
    def save_accounts(self):
        data = {acc_num: vars(acc) for acc_num, acc in self.accounts.items()}  # Convert account objects to a dictionary
        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=4)  # Save the account data to the file

    # Method to create a new account
    def create_account(self, account_holder):
        account_number = str(random.randint(10000000, 99999999))  # Generate a random 8-digit account number
        while account_number in self.accounts:
            account_number = str(random.randint(10000000, 99999999))  # Ensure the account number is unique
        self.accounts[account_number] = BankAccount(account_number, account_holder)  # Create a new account
        self.save_accounts()  # Save the new account to the file
        print(f"Account created successfully. Account Number: {account_number}")

    # Method to find an account by its account number
    def find_account(self, account_number):
        return self.accounts.get(account_number)  # Return the account object if found

    # Main menu for the banking system
    def main_menu(self):
        while True:
            print("\n--- Welcome to the Banking System ---")
            print("1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Transfer Money")
            print("5. Check Balance")
            print("6. Print Receipt")
            print("7. Exit")
            choice = input("Select an option: ")

            if choice == '1':
                account_holder = input("Enter account holder's name: ")
                self.create_account(account_holder)  # Create a new account

            elif choice == '2':
                account_number = input("Enter your account number: ")
                account = self.find_account(account_number)
                if account:
                    amount = float(input("Enter amount to deposit: "))
                    account.deposit(amount)  # Deposit money into the account
                    self.save_accounts()
                else:
                    print("Account not found.")

            elif choice == '3':
                account_number = input("Enter your account number: ")
                account = self.find_account(account_number)
                if account:
                    amount = float(input("Enter amount to withdraw: "))
                    account.withdraw(amount)  # Withdraw money from the account
                    self.save_accounts()
                else:
                    print("Account not found.")

            elif choice == '4':
                account_number = input("Enter your account number: ")
                account = self.find_account(account_number)
                if account:
                    target_account_number = input("Enter the target account number: ")
                    target_account = self.find_account(target_account_number)
                    if target_account:
                        amount = float(input("Enter amount to transfer: "))
                        account.transfer(target_account, amount)  # Transfer money to another account
                        self.save_accounts()
                    else:
                        print("Target account not found.")
                else:
                    print("Account not found.")

            elif choice == '5':
                account_number = input("Enter your account number: ")
                account = self.find_account(account_number)
                if account:
                    print(f"Your balance is: {account.balance}")  # Display the account balance
                else:
                    print("Account not found.")

            elif choice == '6':
                account_number = input("Enter your account number: ")
                account = self.find_account(account_number)
                if account:
                    account.print_receipt()  # Print the account's transaction receipt
                else:
                    print("Account not found.")

            elif choice == '7':
                print("Thank you for using the banking system. Goodbye!")
                break  # Exit the program

            else:
                print("Invalid choice. Please try again.")

# Main entry point of the program
if __name__ == "__main__":
    bank = BankSystem()  # Create an instance of the banking system
    bank.main_menu()  # Start the main menu
