import socket
import threading
import string
import random

HEADER = 64
IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
#SERVER = "192.168.1.12"   #belkin
#SERVER = "192.168.1.12"
SERVER = "192.168.165.141"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNEXT_MSG = '!DISCONNECT'
CREATE_ACC_MSG = '!new'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def check_credentials(msg):
    l = msg.split(" ")
    id_ = l[0].strip()
    passw_ = l[1].strip()
    with open("identification_details.txt", "r") as f:
        for line in f.readlines():
            l = (line.strip()).split(" ")
            str1 = l[0].strip()
            str2 = l[1].strip()
            if (id_==str1 and passw_ == str2):
                print('correct credentials')
                return True
        print("credentials not found")
        return False
            
def append_new(new_id, new_passw):
    with open("identification_details.txt", "a") as f:
        f.write(new_id+" "+new_passw+"\n")

def create_new_account(msg):
    if msg=='doctor':
        new_id = "d"
    else: new_id = "p"
    res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=8))
    #new_id += res
    flag = True
    with open("identification_details.txt", "r") as f:
        for line in f.readlines():
            if new_id+res in line:
                flag = False
                break

        new_passw = ''.join(random.choices(string.ascii_uppercase +string.digits, k=6))
        if flag == True:
            append_new(new_id+res, new_passw)
            return new_id+res+" "+new_passw
        while flag== False:
            res = ''.join(random.choices(string.ascii_uppercase +string.digits, k=8))
            for line in f.readlines():
                if new_id+res in line:
                    flag = False
                    break
            break
        append_new(new_id+res, new_passw)
        return new_id+res+" "+new_passw
            
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")
    connected = True
    flag = False
    f = open('received_file.png', 'wb')
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg==DISCONNEXT_MSG:
                connected = False
                print("i am here, to end")
                break
            elif msg== 'doctor' or msg=='patient':
                print(f"[{addr}] {msg}")
                s = create_new_account(msg)
                print("sending message = ",s)
                message = s.encode(FORMAT)
                msg_length = len(message)
                send_length = str(msg_length).encode(FORMAT)
                send_length = b' ' * (HEADER - len(send_length))
                conn.send(send_length)
                conn.send(message)
                #conn.send(s.encode(FORMAT))
            elif msg== '!pic':
                flag = True
                print(f"[{addr}] {msg}")
            elif msg== '!endpic':
                flag = False
                print(f"[{addr}] {msg}")
            elif flag:
                print("inside flag if")
                print(f"[{addr}] {msg}")
                print("data=%s",(msg))
                if not msg:
                    flag = False
                else:
                    f.write(msg)
            else:
                print(f"[{addr}] {msg}")
                result = check_credentials(msg)
                conn.send(str(result).encode(FORMAT))

    f.close()
    conn.close()
              
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn,addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")
        
        
print("[SERVER] server is starting")
start()