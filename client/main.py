from email import message
import requests
import sys
import os
import utils.utils as utils
import ssl
from urllib.parse import parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler
from datetime import datetime
from multiprocessing import Process
import getpass

API_ENDPOINT = 'https://localhost:3000'
MESSAGE_SERVER_ADDR = '127.0.0.1'
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
    global state
    if state == "unregistered":
        print()

        choice = input("""
                1: Register
                2: Login
                q: Quit

                Please enter your choice: """)

        if choice == "1":
            register()  
        elif choice == "2":
            login()
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
                m: Message a user
                q: Quit

                Please enter your choice: """)

        if choice == "1":
            squareRoot()

        elif choice == "2":
            cubicRoot()

        elif choice == "3":
            nRoot()

        elif choice == "M" or choice == "m":
            sendMessage()
            print("dab")

        elif choice == "Q" or choice == "q":
            state = "unregistered"
            os.system('clear')
            menu()
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

def printSimpleResponse(r):
    os.system('clear')

    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))
    
    print('SERVER RESPONSE: ' + r.text)

    print('')
    menu()

def setUsernamePassword():

    valid = False

    while not valid:
        username = input('Insert a new username: ')
        if username == '' or not username.isalnum():
            print('Please insert a valid username')
        else:
            r = requests.get(url=API_ENDPOINT +
                             '/auth/available/username/' + username, verify=False)
            status = r.status_code
            if status == 200:
                break
            else:
                print('Username is already taken')

    print('')
    valid = False

    while not valid:
        password = getpass.getpass('Insert a password: ')
        if len(password) > 0:
            valid = True

    data = {
        'username': username,
        'password': password
    }

    headers = {
        'authorization': utils.trimPems(certificate)
    }

    r = requests.post(url=API_ENDPOINT +
                      '/auth/set-username-password', data=data, headers=headers, verify=False)

    printSimpleResponse(r)



def printRegisterResponse(r):
    os.system('clear')

    status = r.status_code

    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    if status == 200:
        global state
        state = "registered"

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

        print('SERVER RESPONSE: REGISTRATION SUCCESSFUL')
        print('')
        
        # Open server in new process
        Process(target=openServer, args=('certificate.pem', 'key.key')).start()

        print('SERVER RESPONSE: AUTHENTICATION SUCCESSFUL')

        setUsernamePassword()

    elif status == 404:
        print('SERVER RESPONSE: ' + r.text)
        menu()
    else:
        print('SOMETHING WENT WRONG WITH THE SERVER')
        menu()

    


def register():

    username = input('Username: ')
    onetimeid = input('One time ID: ')

    data = {
        'username': username,
        'oneTimeId': onetimeid
    }

    r = requests.post(url=API_ENDPOINT + '/auth/register',
                      data=data, verify=False)

    printRegisterResponse(r)


def printLoginResponse(r): 
    os.system('clear')

    status = r.status_code

    print(datetime.now().strftime('%d/%m/%Y %H:%M:%S'))

    if status == 200:
        global state
        state = "registered"

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

        print('SERVER RESPONSE: AUTHENTICATION SUCCESSFUL')

        # Open server in new process
        Process(target=openServer, args=('certificate.pem', 'key.key')).start()
    else:
        print('SERVER RESPONSE: ' + r.text)

    print('')
    menu()


def login():
    username = input('Username: ')
    password = getpass.getpass('Password: ')

    data = {
        'username': username,
        'password': password
    }

    r = requests.post(url=API_ENDPOINT + '/auth/login',
                      data=data, verify=False)

    printLoginResponse(r)

def sendMessage():
    valid = False

    address = ''
    port = 0

    while not valid:
        username = input('Insert recipient username: ')
        if username == '' or not username.isalnum():
            print('Please insert a valid username')
        else:
            headers = {
                'authorization': utils.trimPems(certificate)
            }
            params = {
                'username': username
            }
            r = requests.get(url=API_ENDPOINT +
                            '/auth/messageServer', params=params, headers=headers, verify=False)
            status = r.status_code
            if status == 200:
                response_json = r.json()
                address = response_json['address']
                port = response_json['port']
                valid = True
                break
            elif status == 203:
                print('User is offline')
            else:
                print('User is not valid')

    print('')
    valid = False

    while not valid:
        messageBody = input('Type your message: ')
        if len(messageBody) > 0:
            valid = True

    headers = {
        'authorization': utils.trimPems(certificate)
    }

    requests.post(
        url= 'https://' + address + ':' + str(port),
        data= messageBody.encode('utf-8'),
        headers= headers,
        verify= False
        )
    
    menu()

def squareRoot():

    valid = False

    while not valid:
        number = input('Number: ')
        if utils.isNumber(number):
            valid = True
        else:
            print('Please insert a number')

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

    valid = False

    while not valid:
        number = input('Number: ')
        if utils.isNumber(number):
            valid = True
        else:
            print('Please insert a number')

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

    valid = False

    while not valid:
        number = input('Number: ')
        if utils.isNumber(number):
            valid = True
        else:
            print('Please insert a number')

    valid = False

    while not valid:
        index = input('Index (nth root): ')
        if utils.isNumber(index):
            valid = True
        else:
            print('Please insert a number')

    headers = {
        'authorization': utils.trimPems(certificate)
    }

    data = {
        'number': number,
        'index': index
    }

    r = requests.post(
        url=API_ENDPOINT + '/services/nrt',
        headers=headers,
        data=data,
        verify=False
    )
    printServiceResponse(r, 'nRoot')

def openServer(certificateFile, keyFile):
    # Tell server ip and port
    file = open('certificate.pem', mode='r')
    certificate = file.read()
    file.close()

    headers = {
        'authorization': utils.trimPems(certificate)
    }

    data = {
        'ip': MESSAGE_SERVER_ADDR,
        'port': MESSAGE_SERVER_PORT
    }

    requests.post(url=API_ENDPOINT + '/auth/messageServer', data=data, headers=headers, verify=False)

    # Open message server
    httpd = HTTPServer((MESSAGE_SERVER_ADDR, MESSAGE_SERVER_PORT), MessageServerHandler)

    httpd.socket = ssl.wrap_socket(
        httpd.socket,
        keyfile=keyFile,
        certfile=certificateFile,
        server_side=True
        )
    httpd.serve_forever()

class MessageServerHandler(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        
        cert = self.headers['authorization']
        (isAuth, username, full_name) = self.get_sender(cert)

        if isAuth:
            post_data = self.rfile.read(content_length) # <--- Gets the data itself            
            message = post_data.decode('utf-8')
            print('{fullname} ({username}): {message}'.format(fullname= full_name, username= username, message= message))
            
            self._set_response()
            self.wfile.write("Received message".encode('utf-8'))
        else:
            print('Blocked message')
            
            self.send_response(403)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write('Unauthorized'.encode('utf-8'))

    
    def get_sender(self, senderCertificate):
        file = open('certificate.pem', mode='r')
        certificate = file.read()
        file.close()
        
        headers = {
            'authorization': utils.trimPems(certificate)
        }

        data = {
            'certificate': senderCertificate
        }

        r = requests.post(
            url=API_ENDPOINT + '/auth/whoIs',
            headers=headers,
            data=data,
            verify=False
        )

        if r.status_code == 200:
            response_json = r.json()
            return (True, response_json['username'], response_json['full_name'])
        else:
            return (False, '', '')
        

# the program is initiated, so to speak, here
if __name__ == "__main__":
    main()
