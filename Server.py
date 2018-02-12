import socket
from socket import *
import thread
import json
from Customer import Customer
from Account import Account
import re
import threading


list_account = []


def server(connectionSocket, lock):

    try:
        login = connectionSocket.recv(1024)

        data = json.loads(login)

        # take name from client
        temp = data.split(':')[1]
        name = temp.split(',')[0].split(' ')[1]

        # take password from client
        temp = data.split(',')[1]
        password = temp.split(':')[1].split(' ')[1]

        # check if name and password is valid
        if not (re.match("[a-zA-Z0-9]", name) or re.match("[a-zA-Z0-9]", password)):
            connectionSocket.send("0")
            connectionSocket.send("Invalid username and password\n" + "Please try again\n")

        account, customer, msg = customer_login(name, password)
        if msg == "Success":
            # client exist in DB
            while True:
                # always give a menu
                msg = customer_menu()
                connectionSocket.send("1")
                connectionSocket.send(msg)
                # get a client data
                data = connectionSocket.recv(1024)

                data = json.loads(data)

                # take choice from client
                temp = data.split(':')[1]
                choice = int(temp.split(',')[0].split(' ')[1])

                # take amount from client
                temp = data.split(',')[1]
                amount = float(temp.split(':')[1].split(' ')[1])

                msg = account.run_account_options(choice, amount)
                if msg == "Exit":
                    remove_customer_when_exit(account, customer)
                    connectionSocket.send(msg)
                    return
                elif msg != "You have not this amount":
                    # access shared resources (DB)
                    t1 = threading.Thread(target=thread_task, args=(lock, account))
                    t1.start()
                    t1.join()
                connectionSocket.send(msg)

        else:
            # client not exist in DB
            connectionSocket.send("0")
            connectionSocket.send(msg)

        connectionSocket.close()

    except IOError:
        print "something bad happened..."
        connectionSocket.send('404 Not Found')
        connectionSocket.close()


# check if name and password is exist
def customer_login(name, password):
    account, found_customer = search_customers_by_name_and_pass(name, password)
    if found_customer is not None:
        return account, found_customer, "Success"
    else:
        return None, None, "One of the fields you entered is incorrect"
    pass


# preparing a list of accounts and a list of clients
def search_customers_by_name_and_pass(customer_name, password):
    data = json.load(open('DB.json'))
    global list_account
    for account in data:
        balance = data[account]['balance']
        account_name = data[account]['account_name']
        for customer in data[account]['Customers']:
            temp = json.dumps(customer)
            temp = json.loads(temp)
            temp_name = temp['name']
            temp_password = temp['password']
            temp_address = temp['address']
            if temp_name == customer_name and temp_password == password:
                found_customer = Customer(customer_name, password, temp_address)
                return build_list_account(found_customer, balance, account_name)
    return None, None


def customer_menu():
    return "Your Transaction Options Are:\n" + \
            "1) Deposit money\n" + \
            "2) Withdraw money\n" + \
            "3) Check balance\n" + \
            "4) Sign out\n"


def build_list_account(found_customer, balance, account_name):
    if list_account.__len__() != 0:
        for a in list_account:
            if a.get_account_name() == account_name:
                for c in a.get_customer_list():
                    if c.get_name == found_customer.get_name():
                        found_account = a
                        return found_account, found_customer
                found_account = a
                found_account.set_to_list(found_customer)
                return found_account, found_customer
        found_account = Account(found_customer, balance, account_name)
        list_account.append(found_account)
        return found_account, found_customer
    else:
        found_account = Account(found_customer, balance, account_name)
        list_account.append(found_account)
        return found_account, found_customer


# update a balance
def write_to_file(account):
    data = json.load(open('DB.json'))
    for tmp_account in data:
        if account.get_account_name() == data[tmp_account]['account_name']:
            data[tmp_account]['balance'] = account.get_balance()
    with open('DB.json', 'w') as files:
        files.write(json.dumps(data))


def remove_customer_when_exit(account, customer):
    for a in list_account:
        if a is account:
            for c in a.get_customer_list():
                if c is customer:
                    a.remove_from_list(c)
                    if a.get_list().__len__() == 0:
                        list_account.remove(a)
                        break
                    else:
                        break


def thread_task(lock, account):
    lock.acquire()
    write_to_file(account)
    lock.release()


HOST = ''  # host
PORT = 5555  # specifying port
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind((HOST, PORT))
serverSocket.listen(10)
while 1:
    connectionSocket, addr = serverSocket.accept()
    lock = threading.Lock()
    thread.start_new_thread(server, (connectionSocket, lock,))

if __name__ == '__server__':
    server()
