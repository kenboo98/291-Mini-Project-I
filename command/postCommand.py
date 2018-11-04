'''
This command module is for posting ride requests
'''
import sqlite3
import re
import sys

from command.command import Command
from post_requests.post_req import PostReq


class PostCommand(Command):

    def __init__(self, cursor, email):
        super().__init__(cursor)
        self.email = email
        self.pr = PostReq(cursor)
        self.values = {'email': email}
        # functions to ask the user for input. Will be asked in thisd order.
        self.askingFunc = [self.askDate, self.askPickup,
                           self.askDropOff, self.askAmount]

    def menu(self):

        # values of columns
        print('Request Submition: ')
        print('Type "quit" to exit program')
        print('Press Ctrl-c to return to menu')

        for func in self.askingFunc:
            if not func():
                return

        self.pr.insert_req(self.values)
        print('Request has been successfully submitted.')

    def askDate(self):
        while(True):
            date = input("Please input the date in a YYYY-MM-DD form: ")
            if date == 'quit':
                sys.exit()

            matchObj = re.match("(\d){4}-(0\d|1[0-2])-([0-2]\d|3[0-1])", date)
            if matchObj and matchObj.group() == date:
                self.values['rdate'] = date
                return True
            print('Invalid Date')

    def askPickup(self):
        while(True):
            loc = input("Please input the 5 pick up location code: ")
            if loc == 'quit':
                sys.exit()
            if self.pr.validate_location(loc):
                self.values['pickup'] = loc
                return True
            print("Invalid Pickup Location")

    def askDropOff(self):
        while(True):
            loc = input("Please input the 5 destination location code: ")
            if loc == 'quit':
                sys.exit()
            if self.pr.validate_location(loc):
                self.values['dropoff'] = loc
                return True
            print("Invalid Dropoff Location")

    def askAmount(self):
        while(True):
            try:
                inpt = input("Please input your maximum cost per seat: ")
                amnt = int(inpt)
                if amnt < 0:
                    print("Cost cannot be negative.")
                    return False
                self.values['amount'] = amnt
                return True
            except:
                if inpt == 'quit':
                    sys.exit()
                print("Invalid Cost")
