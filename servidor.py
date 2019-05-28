import socket
import threading
import os

host = '0.0.0.0'


def RetrFile(name, sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.send(("EXISTS " + str(os.path.getsize(filename.decode()))).encode())
        userResponse = (sock.recv(1024)).decode()
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "".encode():
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR ".encode())

    sock.close()

def tcpFileTransfer():
    port = 6000
    s = socket.socket()
    s.bind((host,port))
    s.listen(5)
    print("Servidor iniciado.")
    while True:
        c, addr = s.accept()
        print ("IP do cliente conectado:<" + str(addr) + ">")
        t = threading.Thread(target=RetrFile, args=("RetrThread", c))
        t.start()
         
    s.close()

def RetrFileUDP(name, sock):
    filename, addr = sock.recvfrom(1024)
    if os.path.isfile(filename):
        sock.sendto(("EXISTS " + str(os.path.getsize(filename.decode()))).encode(), addr)
        userResponse, addr = sock.recvfrom(1024)
        userResponse = (userResponse).decode()
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.sendto(bytesToSend, addr)
                while bytesToSend != "".encode():
                    bytesToSend = f.read(1024)
                    sock.sendto(bytesToSend, addr)
    else:
        sock.sendto("ERR ".encode())

    sock.close()

def udpFileTransfer():
    port = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host,port))
    print("Servidor iniciado.")
    RetrFileUDP("retrifile",s)
    
         
    s.close()

def Main():

    option2 = input('Você quer utilizar TCP(T) ou UDP(U)? Para sair (S).')
    while True:
        if(option2 == 'U'):
            udpFileTransfer()
        elif(option2 =='T'):
            tcpFileTransfer()
        elif(option2 =='S'):
            break
        else:
            print('Invalid option')
            

if __name__ == '__main__' :
    Main()