import socket 
import threading
import time
import os

START=time.time()
HEADER = 512
PORT = 7003
SERVER = "192.168.0.22"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
PATH="/home/user/Desktop/server/files/"
END="!FINISH"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def Saver(conn,addr, connected):
    name=(conn.recv(HEADER).decode(FORMAT))
    conn.send(f"Caricamento file {name}".encode(FORMAT))
    Writing=True
    with open(PATH+name,"wb") as f:
        print(f"{addr[0]}?query=Save {name}")
        while Writing:
            data=conn.recv(HEADER)
            if data[-7:]==END.encode(FORMAT):
                Writing=False
                data=data[:-7]
            f.write(data)
        f.close()
        print(f"{addr[0]}?status=File saved in {PATH}")

def Send(conn,addr):
    name=(conn.recv(HEADER)).decode(FORMAT)
    print(f"{addr[0]}?query=download {name}")
    f=open(PATH+name, "rb")
    l=f.read(HEADER)
    while (l):
        conn.send(l)
        l=f.read(HEADER)
    f.close()
    conn.send(END.encode(FORMAT))
    print(f"{addr[0]}?status=download completed")

def List():
    pth, dirs, files=next(os.walk(PATH))
    return(str(files))

def stat(thread_start):
    pth, dirs, files=next(os.walk(PATH))
    ret=f"[SERVER] operativo\n[PORTA] {PORT}\n[INDIRIZZO] {SERVER}\n[FILE] {len(files)}\n[ATTIVO DA] {round(time.time()-START,2)}s"
    ret+=f"\n[CLIENT COLLEGATO DA] {round(time.time()-thread_start,2)}s\n[ULTIMA MODIFICA AL SERVER] 2020/08/23 15:12"
    return ret

def handle_client(conn, addr):
    client_start=time.time()
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True
    while connected:
        msg=conn.recv(HEADER).decode(FORMAT)
        if msg==DISCONNECT_MESSAGE:
            print(f"{addr[0]} disconnected")
            conn.send("Disconnessione effettuata".encode(FORMAT))
            break
        elif msg=="file":
            Saver(conn,addr, connected)
        elif msg=="S":
            print(f"{addr[0]}?query=Status")
            conn.send(stat(client_start).encode(FORMAT))
        elif msg=="L":
            print(f"{addr[0]}?query=List")
            conn.send(List().encode(FORMAT))
        elif msg=="D":
            Send(conn, addr)
        else:
            print(f"{addr[0]}?query=Unknown [{msg}]")
            conn.send("Comando non riconosciuto".encode(FORMAT))
    conn.close()
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.activeCount() - 1}")
if __name__=="__main__":
    print("[STARTING] server is starting...")
    start()