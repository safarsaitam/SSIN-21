import requests
import sys
import os
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from datetime import datetime
from multiprocessing import Process

API_ENDPOINT = 'https://localhost:3000'
MESSAGE_SERVER_ADDR = 'localhost'
MESSAGE_SERVER_PORT = 4443

def main():
    print("************Welcome to Application Menu**************")
    menu()

state = "unregistered"

def menu():
    if state == "unregistred":
        print()

        choice = input("""
                1: Register
                q: Quit

                Please enter your choice: """)

        if choice == "1":
            register()

        elif choice == "Q" or choice == "q":
            sys.exit
        else:
            os.system('clear')
            print("Invalid option chosen")
            print("Please try again")
            menu()
    else:
        print()

        choice = input("""
                1: Square root
                2: Cubic root
                3: Nth root
                q: Quit

                Please enter your choice: """)

        if choice == "1":
            squareRoot() 

        elif choice == "2":
            cubicRoot() 

        elif choice == "3":
            nRoot()     

        elif choice == "Q" or choice == "q":
            sys.exit
        else:
            os.system('clear')
            print("Invalid option chosen")
            print("Please try again")
            menu()

def printResponse(r, key):
    os.system('clear')    

    status = r.status_code

    response = r.json()
    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    if status == 200:
        response = r.json()
        print('SERVER RESPONSE: ' + str(response[key]))
    elif status == 403 or status == 404:
        print('SERVER RESPONSE: ' + r.text)
    else:
        print('SOMETHING WENT WRONG WITH THE SERVER')
    
    print('')
    menu()

def register():

    username = input('Username: ')
    onetimeid = input('One time ID: ')

    data = {
        'username': username,
        'oneTimeId': onetimeid
    }

    # Remove verify=False after CA
    r = requests.post(url= API_ENDPOINT + '/auth/register', data=data, verify=False)
    
    response = r.text
    print('')
    print(response)
    print('')

    state = "registred"
    
    # Open server in new process
    Process(target=openServer).start()
    
    menu()


def squareRoot():
    
    username = input('Username: ') # Adapt once CA has been handled
    number = input('Number: ')

    data = {
        'username': username,
        'number': number
    }

    # Remove verify=False after CA
    r = requests.post(url=API_ENDPOINT + '/services/sqrt', data=data, verify=False)
    printResponse(r, 'squareRoot')

def cubicRoot():
    
    username = input('Username: ') # Adapt once CA has been handled
    number = input('Number: ')

    data = {
        'username': username,
        'number': number
    }

    # Remove verify=False after CA
    r = requests.post(url=API_ENDPOINT + '/services/cbrt', data=data, verify=False)
    printResponse(r, 'cubicRoot')

def nRoot():
    
    username = input('Username: ') # Adapt once CA has been handled
    number = input('Number: ')
    index = input('Index (nth root): ')

    data = {
        'username': username,
        'number': number,
        'index': index
    }

    # Remove verify=False after CA
    r = requests.post(url=API_ENDPOINT + '/services/nrt', data=data, verify=False)
    printResponse(r, 'nRoot')        

def openServer():
    # do stuff
    httpd = HTTPServer((MESSAGE_SERVER_ADDR, MESSAGE_SERVER_PORT), SimpleHTTPRequestHandler)

    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        keyfile='',
        certfile='', 
        server_side=True
        )

    httpd.serve_forever()

    print('Opened message server on ' + MESSAGE_SERVER_ADDR + ':' + MESSAGE_SERVER_PORT)
    
    # tell server ip and port
    data = {
        'ip': MESSAGE_SERVER_ADDR,
        'port': MESSAGE_SERVER_PORT
    }

    r = requests.post(url=API_ENDPOINT + '/auth/messageServer', data=data, verify=False)
    printResponse(r, 'Post message server info')


# the program is initiated, so to speak, here
main()
