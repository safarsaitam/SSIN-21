import requests
import sys
import os
import utils.utils as utils
from datetime import datetime

API_ENDPOINT = 'https://localhost:3000'


def main():
    print("************Welcome to Application Menu**************")
    menu()


def menu():
    print()

    choice = input("""
            1: Register
            2: Square root
            3: Cubic root
            4: Nth root
            q: Quit

            Please enter your choice: """)

    if choice == "1":
        register()

    elif choice == "2":
        squareRoot()

    elif choice == "3":
        cubicRoot()

    elif choice == "4":
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

    certificateFile = open('certificate.pem', 'a')
    for line in certificate:
        certificateFile.write(line)
    certificateFile.close()

    global key
    key = response['serviceKey']

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


# the program is initiated, so to speak, here
main()
