import random
from datetime import datetime

class Account:
    """
    A class to represent a generic Bank Account.
    """
    def __init__(self, account_number, account_type, balance=0):
        self.account_number = account_number
        self.account_type = account_type
        self.balance = balance
        self.is_frozen = False
        self.transactions = []

    def deposit(self, amount):
        """Deposit money into the account."""
        if amount > 0:
            self.balance += amount
            self.transactions.append(f"Deposited {amount} on {datetime.now()}")
            print(f"Deposited {amount} to account {self.account_number}. New balance: {self.balance}")
        else:
            print("Deposit amount must be greater than zero.")

    def withdraw(self, amount):
        """Withdraw money from the account."""
        if self.is_frozen:
            print("Account is frozen. Cannot withdraw.")
            return
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"Withdrew {amount} on {datetime.now()}")
            print(f"Withdrew {amount} from account {self.account_number}. New balance: {self.balance}")
        else:
            print("Insufficient funds or invalid withdrawal amount.")

    def atm_withdraw(self, amount):
        """Simulate ATM withdrawal with limits."""
        if self.is_frozen:
            print("Account is frozen. Cannot withdraw from ATM.")
            return
        atm_limit = 1000  # Assume ATM withdrawal limit is 1000
        if amount > atm_limit:
            print(f"ATM withdrawal limit is {atm_limit}. Please try a smaller amount.")
        elif self.balance >= amount:
            self.balance -= amount
            self.transactions.append(f"ATM Withdrawal {amount} on {datetime.now()}")
            print(f"ATM Withdrawn {amount}. New balance: {self.balance}")
        else:
            print("Insufficient funds for ATM withdrawal.")

    def transfer(self, target_account, amount):
        """Transfer money from this account to another account."""
        if self.is_frozen:
            print("Account is frozen. Cannot transfer funds.")
            return
        if amount > 0 and self.balance >= amount:
            self.withdraw(amount)
            target_account.deposit(amount)
            self.transactions.append(f"Transferred {amount} to account {target_account.account_number} on {datetime.now()}")
            print(f"Transferred {amount} from account {self.account_number} to account {target_account.account_number}.")
        else:
            print("Transfer failed. Check if the amount is valid and sufficient funds are available.")

    def freeze_account(self):
        """Freeze the account."""
        self.is_frozen = True
        print(f"Account {self.account_number} has been frozen.")

    def unfreeze_account(self):
        """Unfreeze the account."""
        self.is_frozen = False
        print(f"Account {self.account_number} has been un-frozen.")

    def __str__(self):
        return f"Account[Number: {self.account_number}, Type: {self.account_type}, Balance: {self.balance}, Frozen: {self.is_frozen}]"

    def generate_statement(self):
        """Generate account statement."""
        if not self.transactions:
            print("No transactions for account.")
        else:
            print(f"Account Statement for {self.account_number}:")
            for transaction in self.transactions:
                print(transaction)


class SavingsAccount(Account):
    """Specialized class for Savings Accounts that includes interest calculation."""
    def __init__(self, account_number, balance=0, interest_rate=0.03):
        super().__init__(account_number, "Savings", balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        """Apply interest to the savings account balance."""
        interest = self.balance * self.interest_rate
        self.balance += interest
        self.transactions.append(f"Interest applied {interest} on {datetime.now()}")
        print(f"Applied interest of {interest} to account {self.account_number}. New balance: {self.balance}")


class CheckingAccount(Account):
    """Specialized class for Checking Accounts, which doesn't earn interest."""
    def __init__(self, account_number, balance=0):
        super().__init__(account_number, "Checking", balance)

    def withdraw(self, amount):
        """Override withdraw for checking accounts with an additional fee."""
        fee = 2  # Transaction fee for Checking Accounts
        total_amount = amount + fee
        if self.balance >= total_amount:
            self.balance -= total_amount
            self.transactions.append(f"Withdrew {amount} with a fee of {fee} on {datetime.now()}")
            print(f"Withdrew {amount} with a fee of {fee} from checking account {self.account_number}. New balance: {self.balance}")
        else:
            print("Insufficient funds including the transaction fee.")


class Loan:
    """
    A class to represent a Loan taken by a customer.
    """
    def __init__(self, loan_id, customer, loan_amount, repayment_period):
        self.loan_id = loan_id
        self.customer = customer
        self.loan_amount = loan_amount
        self.repayment_period = repayment_period  # in months
        self.balance = loan_amount
        self.monthly_repayment = loan_amount / repayment_period

    def repay(self, amount):
        """Repay the loan."""
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            print(f"Repayment of {amount} for loan {self.loan_id}. Remaining balance: {self.balance}")
        else:
            print("Invalid repayment amount or loan balance already cleared.")

    def __str__(self):
        return f"Loan[ID: {self.loan_id}, Customer: {self.customer.name}, Amount: {self.loan_amount}, Remaining Balance: {self.balance}]"


class Customer:
    """
    A class to represent a Customer in the bank.
    """
    def __init__(self, customer_id, name, email):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.accounts = []
        self.loans = []

    def add_account(self, account):
        """Add an account to the customer."""
        self.accounts.append(account)
        print(f"Account {account.account_number} added for customer {self.name}.")

    def remove_account(self, account_number):
        """Remove an account from the customer."""
        account_to_remove = next((account for account in self.accounts if account.account_number == account_number), None)
        if account_to_remove:
            self.accounts.remove(account_to_remove)
            print(f"Account {account_number} removed from customer {self.name}.")
        else:
            print(f"Account {account_number} not found for customer {self.name}.")

    def update_info(self, name=None, email=None):
        """Allow customers to update their information."""
        if name:
            self.name = name
        if email:
            self.email = email
        print(f"Customer {self.customer_id} info updated: Name: {self.name}, Email: {self.email}")

    def apply_for_loan(self, loan_amount, repayment_period):
        """Apply for a loan."""
        loan_id = f"L{random.randint(1000, 9999)}"
        loan = Loan(loan_id, self, loan_amount, repayment_period)
        self.loans.append(loan)
        print(f"Loan {loan_id} approved for customer {self.name}. Loan amount: {loan_amount}, Repayment period: {repayment_period} months.")
        return loan

    def __str__(self):
        return f"Customer[ID: {self.customer_id}, Name: {self.name}, Email: {self.email}]"


class Bank:
    """
    A class to represent a Bank that manages customers and accounts.
    """
    def __init__(self, bank_name):
        self.bank_name = bank_name
        self.customers = []
        self.accounts = []

    def add_customer(self, customer):
        """Add a new customer to the bank."""
        self.customers.append(customer)
        print(f"Customer {customer.name} added to {self.bank_name}.")

    def remove_customer(self, customer_id):
        """Remove a customer from the bank."""
        customer_to_remove = next((customer for customer in self.customers if customer.customer_id == customer_id), None)
        if customer_to_remove:
            self.customers.remove(customer_to_remove)
            print(f"Customer {customer_to_remove.name} removed from {self.bank_name}.")
        else:
            print(f"Customer with ID {customer_id} not found.")

    def get_customer(self, customer_id):
        """Retrieve a customer based on customer ID."""
        return next((customer for customer in self.customers if customer.customer_id == customer_id), None)

    def list_customers(self):
        """List all customers in the bank."""
        if self.customers:
            print(f"Customers of {self.bank_name}:")
            for customer in self.customers:
                print(customer)
        else:
            print("No customers found.")


class BankingSystem:
    """
    A class to represent the overall Banking System.
    """
    def __init__(self, bank_name):
        self.bank = Bank(bank_name)
        self.transactions = []

    def process_transaction(self, transaction):
        """Process a bank transaction."""
        self.transactions.append(transaction)
        if transaction.transaction_type == "Deposit":
            transaction.sender_account.deposit(transaction.amount)
        elif transaction.transaction_type == "Withdraw":
            transaction.sender_account.withdraw(transaction.amount)
        elif transaction.transaction_type == "Transfer":
            transaction.sender_account.transfer(transaction.receiver_account, transaction.amount)

    def list_transactions(self):
        """List all transactions."""
        if self.transactions:
            print("Transaction History:")
            for transaction in self.transactions:
                print(transaction)
        else:
            print("No transactions found.")

    def __str__(self):
        return f"BankingSystem[Bank: {self.bank.bank_name}]"
