import requests
import sys
import os
import utils.utils as utils
import ssl
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from datetime import datetime
from multiprocessing import Process

API_ENDPOINT = 'https://localhost:3000'
MESSAGE_SERVER_ADDR = 'localhost'
MESSAGE_SERVER_PORT = 4443


certificate = ''
key = ''
state = ''

def main():
    global state
    state = 'unregistered'

    print("************Welcome to Application Menu**************")
    menu()


def menu():
    if state == "unregistered":
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


def printServiceResponse(r, key):
    os.system('clear')

    status = r.status_code

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


def printRegisterResponse(r):
    os.system('clear')

    status = r.status_code

    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    if status == 200:
        global state
        state = "registered"
    
        # Open server in new process
        # Process(target=openServer).start()

        print('SERVER RESPONSE: REGISTRATION SUCCESSFUL')
    elif status == 404:
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
    r = requests.post(url=API_ENDPOINT + '/auth/register',
                      data=data, verify=False)
    response = r.json()
    global certificate
    certificate = response['certificate']

    if os.path.exists('certificate.pem'):
        os.remove('certificate.pem')

    certificateFile = open('certificate.pem', 'a')
    for line in certificate:
        certificateFile.write(line)
    certificateFile.close()

    global key
    key = response['serviceKey']

    if os.path.exists('key.key'):
        os.remove('key.key')
    
    keyFile = open('key.key', 'a')
    for line in key:
        keyFile.write(line)
    keyFile.close()    

    printRegisterResponse(r)


def squareRoot():

    number = input('Number: ')

    headers = {
        'authorization': utils.trimPems(certificate)
    }

    data = {
        'number': number
    }

    # Remove verify=False after CA
    r = requests.post(
        url=API_ENDPOINT + '/services/sqrt',
        headers=headers,
        data=data,
        verify=False
    )
    printServiceResponse(r, 'squareRoot')


def cubicRoot():

    number = input('Number: ')

    headers = {
        'authorization': utils.trimPems(certificate)
    }

    data = {
        'number': number
    }

    # Remove verify=False after CA
    r = requests.post(
        url=API_ENDPOINT + '/services/cbrt',
        headers=headers,
        data=data,
        verify=False
    )
    printServiceResponse(r, 'cubicRoot')


def nRoot():

    number = input('Number: ')
    index = input('Index (nth root): ')

    headers = {
        'authorization': utils.trimPems(certificate)
    }

    data = {
        'number': number,
        'index': index
    }

    # Remove verify=False after CA
    r = requests.post(
        url=API_ENDPOINT + '/services/nrt',
        headers=headers,
        data=data,
        verify=False
    )
    printServiceResponse(r, 'nRoot')    

# def openServer():
#     # do stuff
#     httpd = HTTPServer((MESSAGE_SERVER_ADDR, MESSAGE_SERVER_PORT), SimpleHTTPRequestHandler)

#     httpd.socket = ssl.wrap_socket(
#         httpd.socket,
#         keyfile='',
#         certfile='', 
#         server_side=True
#         )

#     httpd.serve_forever()

#     print('Opened message server on ' + MESSAGE_SERVER_ADDR + ':' + MESSAGE_SERVER_PORT)
    
#     # tell server ip and port
#     data = {
#         'ip': MESSAGE_SERVER_ADDR,
#         'port': MESSAGE_SERVER_PORT
#     }

#     r = requests.post(url=API_ENDPOINT + '/auth/messageServer', data=data, verify=False)
#     printServiceResponse(r, 'Post message server info')


# the program is initiated, so to speak, here
main()
