import unittest
from datetime import datetime
from random import randint

# Assuming the classes from your provided code are in a file named 'banking_system.py'
from banking_system import Account, SavingsAccount, CheckingAccount, Customer, Loan

class TestBankingSystem(unittest.TestCase):

    def setUp(self):
        """This will run before every test"""
        self.account = Account("123", "Checking", 1000)
        self.savings_account = SavingsAccount("456", 2000)
        self.checking_account = CheckingAccount("789", 1500)
        self.customer = Customer("1", "John Doe", "john.doe@example.com")

    def test_deposit_valid(self):
        """Test deposit of valid amount."""
        initial_balance = self.account.balance
        self.account.deposit(500)
        self.assertEqual(self.account.balance, initial_balance + 500)

    def test_deposit_invalid(self):
        """Test deposit of invalid amount."""
        initial_balance = self.account.balance
        self.account.deposit(-100)
        self.assertEqual(self.account.balance, initial_balance)

    def test_withdraw_valid(self):
        """Test valid withdrawal."""
        initial_balance = self.account.balance
        self.account.withdraw(500)
        self.assertEqual(self.account.balance, initial_balance - 500)

    def test_withdraw_invalid(self):
        """Test withdrawal with insufficient funds."""
        initial_balance = self.account.balance
        self.account.withdraw(2000)
        self.assertEqual(self.account.balance, initial_balance)

    def test_withdraw_frozen_account(self):
        """Test withdrawal from frozen account."""
        self.account.freeze_account()
        initial_balance = self.account.balance
        self.account.withdraw(100)
        self.assertEqual(self.account.balance, initial_balance)

    def test_atm_withdrawal_valid(self):
        """Test valid ATM withdrawal."""
        initial_balance = self.account.balance
        self.account.atm_withdraw(500)
        self.assertEqual(self.account.balance, initial_balance - 500)

    def test_atm_withdrawal_invalid(self):
        """Test ATM withdrawal exceeding limit."""
        initial_balance = self.account.balance
        self.account.atm_withdraw(1500)
        self.assertEqual(self.account.balance, initial_balance)

    def test_transfer_valid(self):
        """Test transfer between accounts."""
        target_account = Account("456", "Savings", 1000)
        initial_balance_sender = self.account.balance
        initial_balance_receiver = target_account.balance
        self.account.transfer(target_account, 500)
        self.assertEqual(self.account.balance, initial_balance_sender - 500)
        self.assertEqual(target_account.balance, initial_balance_receiver + 500)

    def test_transfer_invalid(self):
        """Test transfer with insufficient funds."""
        target_account = Account("456", "Savings", 1000)
        initial_balance_sender = self.account.balance
        self.account.transfer(target_account, 2000)
        self.assertEqual(self.account.balance, initial_balance_sender)

    def test_freeze_account(self):
        """Test freezing an account."""
        self.account.freeze_account()
        self.assertTrue(self.account.is_frozen)

    def test_unfreeze_account(self):
        """Test unfreezing an account."""
        self.account.freeze_account()
        self.account.unfreeze_account()
        self.assertFalse(self.account.is_frozen)

    def test_savings_interest(self):
        """Test interest application on savings account."""
        initial_balance = self.savings_account.balance
        self.savings_account.apply_interest()
        expected_balance = initial_balance * (1 + self.savings_account.interest_rate)
        self.assertEqual(self.savings_account.balance, expected_balance)

    def test_checking_account_fee(self):
        """Test transaction fee on checking account withdrawal."""
        initial_balance = self.checking_account.balance
        self.checking_account.withdraw(100)
        self.assertEqual(self.checking_account.balance, initial_balance - 102)  # 100 + 2 fee

    def test_customer_add_account(self):
        """Test adding an account to a customer."""
        initial_accounts_count = len(self.customer.accounts)
        self.customer.add_account(self.account)
        self.assertEqual(len(self.customer.accounts), initial_accounts_count + 1)

    def test_customer_remove_account(self):
        """Test removing an account from a customer."""
        self.customer.add_account(self.account)
        initial_accounts_count = len(self.customer.accounts)
        self.customer.remove_account(self.account.account_number)
        self.assertEqual(len(self.customer.accounts), initial_accounts_count - 1)

    def test_customer_apply_for_loan(self):
        """Test applying for a loan."""
        loan = self.customer.apply_for_loan(5000, 12)
        self.assertEqual(loan.loan_amount, 5000)
        self.assertEqual(loan.repayment_period, 12)

    def test_loan_repayment(self):
        """Test loan repayment."""
        loan = self.customer.apply_for_loan(5000, 12)
        initial_balance = loan.balance
        loan.repay(500)
        self.assertEqual(loan.balance, initial_balance - 500)

    def test_loan_invalid_repayment(self):
        """Test invalid loan repayment."""
        loan = self.customer.apply_for_loan(5000, 12)
        initial_balance = loan.balance
        loan.repay(6000)  # Trying to repay more than the loan balance
        self.assertEqual(loan.balance, initial_balance)

if __name__ == "__main__":
    unittest.main()
