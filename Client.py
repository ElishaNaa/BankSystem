import socket
from socket import *
import sys
import thread
import json
import re
import time


def client():
    HOST = "localhost"
    PORT = 5555
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.connect((HOST, PORT))

    login = run_login()

    # take name from client
    temp = login.split(':')[1]
    name = temp.split(',')[0].split(' ')[1]

    # take password from client
    temp = login.split(',')[1]
    password = temp.split(':')[1].split(' ')[1]

    # check if name and password is valid
    if not (re.match("[a-zA-Z0-9]", name) or re.match("[a-zA-Z0-9]", password)):
        print "Invalid username and password\n" + "Please try again\n"
        client()

    serverSocket.send(login)
    flag = serverSocket.recv(1024)
    data = serverSocket.recv(1024)

    while flag == "1":
        action = check_legal(data)
        while action == "0":
            print "Not illegal"
            action = check_legal(data)

        serverSocket.send(action)
        msg = serverSocket.recv(1024)
        if msg == "Exit":
            print "We were happy to serve you"
            serverSocket.close()
            return
        else:
            print '\n' + msg
            flag = serverSocket.recv(1024)
            data = serverSocket.recv(1024)
    print data
    client()


# check if the amount legal, update and send to client message accordingly
def run_account_options(option):
    choice = int(option)
    if choice == 1:
        try:
            amount = float(input("::\nPlease enter amount to be deposited\n: "))
            if amount > 0:
                choice = 'choice: ' + str(choice) + ', '
                amount = 'amount: ' + str(amount)
                temp = choice + amount
                msg = json.dumps(temp)
                return msg
            else:
                return "0"
        except:
            return "0"
    elif choice == 2:
        try:
            amount = float(input("::\nPlease enter the amount you want to withdraw\n: "))
            if amount > 0:
                choice = 'choice: ' + str(choice) + ', '
                amount = 'amount: ' + str(amount)
                temp = choice + amount
                msg = json.dumps(temp)
                return msg
            else:
                return "0"
        except:
            return "0"
    elif choice == 3:
        msg = 'choice: ' + str(choice) + ', '
        msg = json.dumps(msg + 'amount: ' + str(0))
        return msg
    elif choice == 4:
        msg = 'choice: ' + str(choice) + ', '
        msg = json.dumps(msg + 'amount: ' + str(0))
        return msg


# page to login
def run_login():
    name = raw_input("\nPlease input customer name: ")
    password = raw_input("\nPlease input customer password: ")
    msg = 'name: ' + name + ', '
    msg = json.dumps(msg + 'password: ' + password)
    return msg


# check if choice's client is legal
def check_legal(data):
    try:
        option = int(raw_input(data))
        if 0 < option < 5:
            action = run_account_options(option)
            return action
        else:
            return "0"
    except:
        return "0"


if __name__ == '__main__':
    client()
