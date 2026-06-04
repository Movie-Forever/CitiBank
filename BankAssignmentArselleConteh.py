from abc import ABC, abstractmethod

# interface for transactions
class ITransaction(ABC):
    @abstractmethod
    def print_receipt(self):
        pass

# customers should have a name and account information
class Customer:
    def __init__(self, customer_id, first_name, last_name):
        self.customer_id = customer_id
        self.first_name = first_name
        self.last_name = last_name
        self.accounts = []

# base account class
class Account(ITransaction):
    def __init__(self, account_number, account_holder, balance=0):
        self.account_number = account_number
        self.account_holder = account_holder
        self.balance = balance
    
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited ${amount}. New balance: ${self.balance}")
        else:
            print("Amount must be positive")
    
    @abstractmethod
    def withdraw(self, amount):
        pass
    
    def print_receipt(self):
        print(f"Account: {self.account_number} | Holder: {self.account_holder.first_name} | Balance: ${self.balance}")

# savings accounts
class SavingsAccount(Account):
    def __init__(self, account_number, account_holder, balance=0, interest_rate=0.02):
        super().__init__(account_number, account_holder, balance)
        self.interest_rate = interest_rate
    
    def withdraw(self, amount):
        if self.balance - amount < 100:
            print("Cannot withdraw - minimum balance must be $100")
        elif amount > 0:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print("Amount must be positive")

# checking accounts
class CheckingAccount(Account):
    def __init__(self, account_number, account_holder, balance=0, overdraft_limit=500):
        super().__init__(account_number, account_holder, balance)
        self.overdraft_limit = overdraft_limit
    
    def withdraw(self, amount):
        if self.balance - amount >= -self.overdraft_limit:
            self.balance -= amount
            print(f"Withdrew ${amount}. New balance: ${self.balance}")
        else:
            print(f"Exceeds overdraft limit of ${self.overdraft_limit}")

# put it all together in a bank class.
class Bank:
    def __init__(self):
        self.customers = []
        self.seed_data()
    
    def seed_data(self):
        c1 = Customer(1, "John", "Doe")
        c2 = Customer(2, "Jane", "Smith")
        
        c1.accounts.append(SavingsAccount("S001", c1, 1000))
        c2.accounts.append(CheckingAccount("C001", c2, 500))
        
        self.customers.append(c1)
        self.customers.append(c2)
    
    def find_account(self, account_number):
        for customer in self.customers:
            for account in customer.accounts:
                if account.account_number == account_number:
                    return account
        return None
    
    def create_account(self):
        try:
            cust_id = int(input("Enter Customer ID: "))
            customer = None
            for c in self.customers:
                if c.customer_id == cust_id:
                    customer = c
                    break
            
            if not customer:
                print("Customer not found")
                return
            
            acc_num = input("Enter Account Number: ")
            acc_type = input("Savings (S) or Checking (C)? ").upper()
            balance = float(input("Initial Balance: "))
            
            if acc_type == "S":
                account = SavingsAccount(acc_num, customer, balance)
            else:
                account = CheckingAccount(acc_num, customer, balance)
            
            customer.accounts.append(account)
            print("Account created successfully")
        except ValueError:
            print("Invalid input")
    
    def view_all_accounts(self):
        if not self.customers:
            print("No customers found")
            return
        
        for customer in self.customers:
            print(f"\nCustomer: {customer.first_name} {customer.last_name}")
            for account in customer.accounts:
                account.print_receipt()
    
    def deposit(self):
        try:
            acc_num = input("Enter Account Number: ")
            account = self.find_account(acc_num)
            if account:
                amount = float(input("Enter amount: "))
                account.deposit(amount)
            else:
                print("Account not found")
        except ValueError:
            print("Invalid input")
    
    def withdraw(self):
        try:
            acc_num = input("Enter Account Number: ")
            account = self.find_account(acc_num)
            if account:
                amount = float(input("Enter amount: "))
                account.withdraw(amount)
            else:
                print("Account not found")
        except ValueError:
            print("Invalid input")
    
    def transfer(self):
        try:
            source_acc = input("Source Account Number: ")
            dest_acc = input("Destination Account Number: ")
            amount = float(input("Amount to transfer: "))
            
            source = self.find_account(source_acc)
            dest = self.find_account(dest_acc)
            
            if source and dest:
                source.withdraw(amount)
                if source.balance >= 0 or isinstance(source, CheckingAccount):
                    dest.deposit(amount)
                    print("Transfer complete")
            else:
                print("Account not found")
        except ValueError:
            print("Invalid input")
    
    def close_account(self):
        acc_num = input("Enter Account Number to close: ")
        for customer in self.customers:
            for i, account in enumerate(customer.accounts):
                if account.account_number == acc_num:
                    customer.accounts.pop(i)
                    print("Account closed")
                    return
        print("Account not found")
    
    def run(self):
        print("=" * 50)
        print("Welcome to My Bank")
        print("=" * 50)
        
        while True:
            print("\n1) Create Account")
            print("2) View All Accounts")
            print("3) Deposit")
            print("4) Withdraw")
            print("5) Transfer")
            print("6) Close Account")
            print("7) Exit")
            
            try:
                choice = input("\nSelect option: ")
                
                if choice == "1":
                    self.create_account()
                elif choice == "2":
                    self.view_all_accounts()
                elif choice == "3":
                    self.deposit()
                elif choice == "4":
                    self.withdraw()
                elif choice == "5":
                    self.transfer()
                elif choice == "6":
                    self.close_account()
                elif choice == "7":
                    print("Thank you for banking with us!")
                    break
                else:
                    print("Invalid option")
            except Exception as e:
                print(f"Error: {e}")

def main():
    bank = Bank()
    bank.run()

if __name__ == "__main__":
    main()