import os
import sqlite3
import time
import sys
import datebase

def clear(): return os.system('cls')

#===============CONNECT SQL ===========================
if os.path.exists('Messanger.db'):
    conn = sqlite3.connect('Messanger.db')
    cursor = conn.cursor()
else:
    datebase.create()
    conn = sqlite3.connect('Messanger.db')
    cursor = conn.cursor()
#=====================USER============================
class User():
    def __init__(self, id, name, password, phone):  # self = id >= sql
        self.id = id
        self.name = name
        self.password = password
        self.phone = phone
#***************INBOX***********
    def inbox(self):
        clear()
        print(4*"*","INBOX",4*"*")
        sql = "SELECT Message.ID , Users.Name, Message.seen from Message inner join Users on ID_tra=Users.ID WHERE ID_rec=?"
        a = cursor.execute(sql,(self.id,))
        for idx,user,seen in a:
            if seen == 1:
                print(f'{idx} . {user} .(New)')
            else:
                print(f'{idx} . {user}')
        print('0. Back To Menu')
        sel = input("Select your Message: ")
        if sel !='0':
            try:
                show_msg = Message.fromDB(self.id, sel)
                show_msg.show()
            except:
                print("Wrong Message Number")
                time.sleep(1.5)
                self.inbox()
        else:
            pass
#*********COMPOSE*************
    def compose(self):
        clear()
        print(4*"*","CONPOSE",4*"*")
        print("Enter Your TEXT:")
        msg = input()
        sql = "SELECT Friends.ID_f, Users.Name FROM Friends INNER JOIN Users ON Friends.ID_F =Users.ID WHERE Sours_ID =?"
        a = cursor.execute(sql,(self.id,))
        for idx, i in enumerate(a):
            print(f'{idx+1} . Name : {i[1]} , ID:  {i[0]}')
        tra = input('Select ID Friends: ')
        t= time.localtime()
        time_send =time.strftime("%H:%M   %d/%m", t)
        newmess = Message.sending(self.id, tra, msg,time_send)
        newmess.send()
        #print("ID Friend Not Found! ")
        #time.sleep(1.5)
        #self.compose()
#*************ADD FRIEND*************
    def add_friend(self):
        clear()
        print(4*"*","ADD FRIEND",4*"*")
        show_users = cursor.execute('SELECT ID , Name FROM Users WHERE ID!=?',(self.id,))
        for idx, i in enumerate(list(show_users)):
            print(f'{idx+1} . ID: {i[0]} Name:{i[1]}')
        print("0_ Menu")
        id_f = input('enter Your friends ID : ')
        if id_f !='0':
            sql = "INSERT INTO Friends(Sours_ID , ID_F) VALUES (?,?)"
            cursor.execute(sql,(self.id, id_f))
            conn.commit()
            print(f"{id_f} Added Yo Your Friends")
            for i in range(5):
                print('.',end = ' ')
                time.sleep(0.5)
        else:
            pass
#**************SHOW FRIEND*************
    def show_friend(self):
        print(4*"*","YOUR FRIENDS",4*"*")
        sql = "SELECT Friends.ID_f, Users.Name FROM Friends INNER JOIN Users ON Friends.ID_F =Users.ID WHERE Sours_ID =?"
        a = cursor.execute(sql,(self.id,))
        for idx, i in enumerate(list(a)):
            print(f'{idx+1} . Name : {i[1]} , ID:  {i[0]}')
        print('0- Back Menu')
        while True:
            bk=input()
            if bk=="0":
                break
    #************EDIT NAME**********
    def edit_name(self):
        print(4*'*','EDIT NAME',4*'*')
        new_name =input('Enter New name:')
        sql ='UPDATE Users SET Name =? WHERE ID=?'
        cursor.execute(sql,(new_name,self.id))
        conn.commit()
        print('Your Name Has Been Changed')
        for i in range(7):
            print('.',end = ' ')
            time.sleep(0.5)
        return new_name
#****************EDIT PASSWORD***********
    def edit_password(self):
        print(4*'*','EDIT PASSWORD',4*'*')
        old_password =input('Enter Last password:')
        new_password =input('Enter New password:')
        new_password2 =input('Enter Again New password:')
        if new_password==new_password2:
            sql ='UPDATE Users SET Password =? WHERE ID=?'
            cursor.execute(sql,(new_password,self.id))
            conn.commit()
            print('Your Password Has Been Changed')
            for i in range(7):
                print('.',end = ' ')
                time.sleep(0.5)
        else:
            print("Password Not Match!")
            time.sleep(1.5)
            clear()
            self.edit_password()
#***************EDIT PHONE**************
    def edit_phone(self):
        print(4*'*','EDIT PHONE',4*'*')
        new_phone =input('Enter New Phone:')
        sql ='UPDATE Users SET phone =? WHERE ID=?'
        cursor.execute(sql,(new_phone,self.id))
        conn.commit()
        print('Your phone Has Been Changed')
        for i in range(7):
            print('.',end = ' ')
            time.sleep(0.5)
    def log_out(self):
        ch = input('Are You sSre? (y/n): ')
        if ch == 'y':
            clear()
            Application()

#=======================MESSAGE=======================
class Message():
    def __init__(self, id_tra, id_rec,txt,time,name_tra,msg_id):
        self.id_tra = id_tra
        self.name_tra=name_tra
        self.id_rec = id_rec
        self.txt = txt
        self.time =time
        self.msg_id = msg_id
    @classmethod
    def fromDB(Class,userid,msg_id):
        sql = "SELECT Message.Text , Users.Name,Message.time , Message.ID_tra FROM Message INNER JOIN Users on ID_tra = Users.ID WHERE Message.ID =? AND Message.ID_rec = ?"
        a = cursor.execute(sql,(msg_id ,userid))
        for i in a:
            sql = "UPDATE Message SET Seen = 0 WHERE ID =?"
            cursor.execute(sql,(msg_id))
            conn.commit()
            return Class(i[3],userid,i[0],i[2],i[1],msg_id)
    @classmethod
    def sending(Class,tra,rec,text,time):
        return Class(tra,rec,text,time,'',0)
#****************SHOW MESSAGE ****************
    def show(self):
        clear()
        print(4*"*","TEXT MESSAGE",4*"*")
        print(f'Name : {self.name_tra}')
        print(f'Text  {self.txt}')
        print(f'AT : {self.time}')
        print('1- Reply     ','2- Forward   ','3- delete    ','4- Menu')
        ch = input('Enter your selection:')
        if ch == '1':
            self.compose_reply()
        elif ch == '2':
            self.forward()
        elif ch == '3':
            n = input("DELETE MESSAGE?!?(Y/N): ")
            if n =='y':
                sql = 'DELETE FROM Message WHERE ID=?'
                cursor.execute(sql,(self.msg_id))
                conn.commit()
            else:
                self.show()
        elif ch=='4':
            pass
#***********COMPOSE REPLY************************
    def compose_reply(self):
        clear()
        print(4*"*","REPLY",4*"*")
        print("Enter Your TEXT:")
        msg = input()
        t= time.localtime()
        time_send =time.strftime("%H:%M   %d/%m",t)
        try:
            sql = "INSERT INTO Message(Text,ID_rec,ID_tra,time,Seen) Values (?,?,?,?,1)"
            cursor.execute(sql,(msg, self.id_tra, self.id_rec,time_send))
            conn.commit()
        except:
            print("Sorry! can't send Message")
            time.sleep(2)
        else:
            for i in range(6):
                print('.',end = ' ')
                time.sleep(0.5)
            print("Message Sent")
            time.sleep(1.2)
#*******************FORWARD MESSAGE*****************
    def forward(self):
        clear()
        print(4*"*","FORWARD",4*"*")
        sql = "SELECT Friends.ID_f, Users.Name FROM Friends INNER JOIN Users ON Friends.ID_F =Users.ID WHERE Sours_ID =?"
        a = cursor.execute(sql,(self.id_rec,))
        for idx, i in enumerate(list(a)):
            print(f'{idx+1} . Name : {i[1]} , ID:  {i[0]}')
        tra = input('Select ID Friends: ')
        t= time.localtime()
        time_send =time.strftime("%H:%M   %d/%m",t)
        sql = "INSERT INTO Message(Text,ID_rec,ID_tra,time,Seen) VALUES (?,?,?,?,1)"
        cursor.execute(sql,(self.txt , tra , self.id_rec,time_send))
        conn.commit()
        for i in range(6):
            print('.',end = ' ')
            time.sleep(0.5)
        print("Message Sent")
        time.sleep(1.2)
#***************SEND MESSAGE***************************
    def send(self):
        sql = "INSERT INTO Message(Text,ID_rec,ID_tra,time,Seen) VALUES (?,?,?,?,1)"
        cursor.execute(sql,(self.txt, self.id_rec, self.id_tra,self.time))
        conn.commit()
        for i in range(6):
            print('.',end = ' ')
            time.sleep(0.5)
        print("Message Sent")
        time.sleep(1.2)
#===============APPLICATION=============
class Application():
    def __init__(self):
        self.user = None
        self.login_menu()
#************LOGIN*********
    def login(self):
        print(4*'*','Login',4*'*')
        user_id = input('Enter ID : ').lower()
        self.id_source = user_id
        password = input('Enter Password : ')
        sql = "SELECT Name, phone FROM Users WHERE ID=? AND Password=?"
        log = cursor.execute(sql,(user_id,password))
        for i in log:
            self.name_user = i[0]
            phone = i[1]
            self.user = User(self.id_source, self.name_user, password, phone)
        return self.user
#*************SING_UP***********
    def sing_up(self):
        print(4*'*','Sing_UP',4*'*')
        self.name_user = input('Enter Name : ')
        password = input('Enter Password : ')
        password2 = input('Enter Password Again:')
        while password != password2:
            print("Password Not Math")
            password = input('Enter Password : ')
            password2 = input('Enter Password Again:')
        self.id_source = input('Enter your ID: ').lower()
        tel = input('Enter Your Phone Number: ')
        sql ="INSERT INTO Users VALUES(?,?,?,?)"
        cursor.execute(sql,(self.id_source,self.name_user,password,tel))
        conn.commit()
        self.user = User(self.id_source, self.name_user , password, tel)
        return self.user
#*************LOGIN MENU*************
    def login_menu(self):
        while True:
            print(4*"*","WELLCOME",4*"*")
            print('1- Login')
            print('2- Sing UP')
            ch = input("Enter your selection: ")
            clear()
            if ch == '1':
                user = self.login()
                for i in range(5):
                    print('.',end = ' ')
                    time.sleep(0.5)
                if user:
                    break
                else:
                    print('User or password is incorrect')
                    time.sleep(2)
                    clear()
            elif ch == '2':
                user = self.sing_up()
                for i in range(6):
                    print('.',end = ' ')
                    time.sleep(0.5)
                if user:
                    break
        self.main()
#*************SETTING MENU***********
    def setting_menu(self):
        while True:
            clear()
            print(4*"*","SETTING",4*"*")
            print('1- Edit Name')
            print('2- Edit Password')
            print('3- Edit Phone')
            print('4- Log_out')
            print('0- Back Menu')
            ch = input('Enter Your Selection: ')
            if ch == '1':
                clear
                name_new= self.user.edit_name()
                self.name_user=name_new
                break
            elif ch == '2':
                clear()
                self.user.edit_password()
                break
            elif ch == '3':
                clear()
                self.user.edit_phone()
                break
            elif ch == '4':
                clear()
                self.user.log_out()
                break
            elif ch == '0':
                self.main()
            else:
                self.setting_menu()
        self.main()
#***************MAIN*************
    def main(self):
        while True:
            clear()
            print(4*"*","MENU",4*"*")
            print('USER ID:',self.id_source ,'USER NAME:',self.name_user)
            print('1-Inbox')
            print('2-Friends')
            print('3-Add Friends')
            print('4-Compose')
            print('5-Seting')
            print('0-EXIT')
            ch = input('Enter your selection: ')
            print('*'*30)
            if ch == '1':
                self.user.inbox()
            elif ch == '2':
                clear()
                self.user.show_friend()
            elif ch == '3':
                self.user.add_friend()
            elif ch== '4':
                self.user.compose()
            elif ch== '5':
                self.setting_menu()
            elif ch =='0':
                sys.exit(0)
#===========RUN==============
if __name__ == "__main__":
    app = Application()