import requests
import sys

def main():
    menu()


def menu():
    print("************Welcome to Application Menu**************")
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
        print("Invalid option chosen")
        print("Please try again")
        menu()


def register():

    username = input('Username: ')
    onetimeid = input('One time ID: ')

    data = {
        'username': username,
        'oneTimeId': onetimeid
    }

    r = requests.post(url='https://localhost:3000/auth/register', data=data, verify=False)
    
    response = r.text
    print('')
    print(response)
    print('')
    menu()


def login():
    pass


# the program is initiated, so to speak, here
main()
