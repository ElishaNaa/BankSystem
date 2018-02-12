class BankService:

    def deposit(self, amount):
        if self.balance - amount > 0:
            self.balance += amount
        else:
            print("amount not illegal")

    def withdraw(self, amount):
        if self.balance - amount > 0:
            self.balance -= amount
        else:
            print("amount not illegal")

    def print_balance(self):
        print("Your account balance is %.2f" % self.balance)
