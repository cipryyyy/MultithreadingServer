import socket
import os
from tkinter import Tk, filedialog, Button

HEADER = 512
PORT = 7003
SERVER = "192.168.0.22"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
CLOSER = "!DISCONNECT"
END = "!FINISH"
SAVE = "C:\\Users\\User\\Documents\\Server downloads\\"

path=None
directory=None
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
client.settimeout(5)
client.connect(ADDR)

def Browser():
    global directory
    filename=filedialog.askopenfilename(title="Seleziona il file da caricare", filetypes = (("Immagini", "*.jpg* *.cr2* *.png*"), ("Documenti", "*.txt* *.doc* *.odt*"), ("all files", "*.*")))
    if filename:
        directory=filename
    root.destroy()

def File():
    root=Tk()
    root.title("Seleziona il file da caricare")
    root.geometry("200x100")

    button=Button(root, text="Upload", command=Browser).pack()
    root.mainloop()
    print(directory)

    name=os.path.basename(directory)
    client.send("file".encode(FORMAT))
    client.send(name.encode(FORMAT))
    print(client.recv(HEADER).decode(FORMAT))
    f=open(directory,"rb")
    l=f.read(HEADER)
    while (l):
        client.send(l)
        l=f.read(HEADER)
    f.close()
    client.send(END.encode(FORMAT))
    print("File caricato")

def Saver(path):
    client.send("D".encode(FORMAT))
    name=input("File da scaricare:\t")
    client.send(name.encode(FORMAT))
    Writing=True
    with open(path+name, "wb") as f:
        while Writing:
            data=client.recv(HEADER)
            if data[-7:]==END.encode(FORMAT):
                data=data[:-7]
                break
            f.write(data)
        f.close()
    print(f"File salvato in {path}")

def send(msg):
    client.send((msg.encode(FORMAT)).upper())
    print(client.recv(HEADER).decode(FORMAT))

def main():
    cmd=input("-->\t")
    if not cmd:
        cmd=input("-->\t")
    elif cmd.upper()=="E":
        send(CLOSER)
        quit()
    elif cmd.upper()=="F":
        File()
    elif cmd.upper()=="D":
        Saver(SAVE)
    else:
        send(cmd)

if __name__=="__main__":
    while True:
        main()