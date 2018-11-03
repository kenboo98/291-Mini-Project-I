import sqlite3
import sys
import os.path
from authentication.member import Member
from command.memberCommand import MemberCommand

from command.postCommand import PostCommand


connection = None
cursor = None

mCmd = None
pCmd = None

user = None

def connect(path):
    global connection, cursor, mCmd, pCmd

    connection = sqlite3.connect(path)
    cursor = connection.cursor()
    cursor.execute(' PRAGMA forteign_keys=ON; ')
    connection.create_function('HASH', 1, Member.hash)
    connection.commit()

    mCmd = MemberCommand(cursor)
    pCmd = PostCommand(cursor, "kenboo1998@gmail.com")
    return

def main():
    global connection, cursor

    db_path = "./prj.db"
    if os.path.isfile(db_path):
        connect(db_path)
    else:
        print('ERROR: database file not found')
        sys.exit(0)

    pCmd.ask()

    connection.commit()
    connection.close()
    return

if __name__ == "__main__":
    main()
