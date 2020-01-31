import sqlite3
def create():
    conn = sqlite3.connect('Messanger.db')
    conn.execute('''CREATE TABLE Users
            (ID    nvarchar(50) PRIMARY KEY     NOT NULL,
            NAME           nvarchar(50)    NOT NULL,
            Password            nvarchar(50)     NOT NULL,
            Phone        nvarchar(12));''')

    conn.execute('''CREATE TABLE Friends
            (ID    INTEGER  PRIMARY KEY  AUTOINCREMENT,
            Sours_ID           nvarchar(50)    NOT NULL,
            ID_F            nvarchar(50)     NOT NULL,
            FOREIGN KEY(ID_F) REFERENCES User(ID));''')

    conn.execute('''CREATE TABLE Message
            (ID    INTEGER  PRIMARY KEY  AUTOINCREMENT,
            Text           nvarchar(200)    NOT NULL,
            ID_rec           nvarchar(50)    NOT NULL,
            ID_tra            nvarchar(50)     NOT NULL,
            time            nvarchar(25)     NOT NULL,
            Seen            bit     NOT NULL,
            FOREIGN KEY(ID_tra) REFERENCES User(ID));''')
