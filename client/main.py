import requests
import sys
import os
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
    


# the program is initiated, so to speak, here
main()
