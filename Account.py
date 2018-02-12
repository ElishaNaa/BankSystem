from Customer import Customer


class Account:

    def __init__(self, customer, balance, account_name):
        self.balance = float(balance)
        self.account_name = account_name
        self.list_customer = []
        if self.list_customer.__len__() != 0:
            flag = 0
            for c in self.list_customer:
                if c.get_name() == customer.get_name():
                    flag = 1
                    break
            if flag != 1:
                self.list_customer.append(customer)
        else:
            self.list_customer.append(customer)

    def set_to_list(self, customer):
        if self.list_customer.__len__() != 0:
            flag = 0
            for c in self.list_customer:
                if c.get_name() == customer.get_name():
                    flag = 1
                    break
            if flag != 1:
                self.list_customer.append(customer)
        else:
            self.list_customer.append(customer)

    def deposit(self, amount):
        if self.balance + amount > 0:
            self.balance += amount
        else:
            return "amount not illegal"

    def withdraw(self, amount):
        if self.balance - amount > 0:
            self.balance -= amount
        else:
            return "amount not illegal"

    def print_balance(self):
        return "Your account balance is " + str(self.balance)

    def get_balance(self):
        return self.balance

    def get_account_name(self):
        return self.account_name

    def run_account_options(self, choice, amount):
        if choice == 1:
            if amount > 0:
                self.deposit(amount)
                return self.print_balance()
            else:
                return "amount not illegal"
        elif choice == 2:
            if amount > 0:
                if "amount not illegal" == self.withdraw(amount):
                    return "You have not this amount"
                return self.print_balance()
            else:
                return "amount not illegal"
        elif choice == 3:
            return self.print_balance()
        elif choice == 4:
            return "Exit"

    def get_customer_list(self):
        return self.list_customer

    def remove_from_list(self, customer):
        for c in self.list_customer:
            if c.get_name() == customer.get_name():
                self.list_customer.remove(customer)
                break

    def get_list(self):
        return self.list_customer
