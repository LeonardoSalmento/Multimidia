import os
import re
import time
import socket
from platform import system as system_name 
from subprocess import call as system_call  
import subprocess

host = '127.0.0.1'

def transferenciaTcp():
   
    porta = 6000

    s = socket.socket()
    s.connect((host, porta))


    filename = input("Qual o nome do arquivo? -> ").encode()
    if filename != 'q'.encode():
        s.send(filename)
        data = s.recv(1024)
        if data[:6] == 'EXISTS'.encode():
            filesize = int(data[6:].decode())
            message = input("O arquivo possui tamanho = " + str(filesize) +"Bytes, Deseja enviar? (S/N)? -> ")
            if message == 'S':
                s.send("OK".encode())
                f = open('new_'+filename.decode(), 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done", end='\r')
                print("Arquivo Enviado!")
                f.close()
        else:
            print ("Arquivo não existe!")

    s.close()

def transferenciaUdp():
    porta = 5001

    server = (host,5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    filename = input("Qual o nome do arquivo? -> ").encode()
    if filename != 'q'.encode():
        s.sendto(filename,server)
        data, addr = s.recvfrom(1024)
        if data[:6] == 'EXISTS'.encode():
            filesize = int(data[6:].decode())
            message = input("O arquivo possui tamanho = " + str(filesize) +"Bytes, Deseja enviar? (S/N)? -> ")
            if message == 'S':
                s.sendto("OK".encode(), addr)
                f = open('new_'+filename.decode(), 'wb')
                data, addr = s.recvfrom(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < filesize:
                    data, addr = s.recvfrom(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done", end='\r')
                print("Arquivo Enviado!")
                f.close()
        else:
            print ("Arquivo não existe!")

    s.close()


def taxaTransferencia(ip, porta):                              
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp.connect((ip,porta))
    teste = "0"*1024*1024*10
    begin = time.time()
    tcp.send(teste.encode())
    end = time.time()
    tcp.close()
    time_to_send = (end-begin)
    transferRatio = 8/time_to_send

    if transferRatio>100:
        print("A melhor opção, é utilizar o TCP")
        transferenciaUdp()
    else:
        print("A melhor opção é utilizar o UDP")
        transferenciaUdp()

    return transferRatio


def Main():
    taxaTransferencia('127.0.0.1',6000)








if __name__ == '__main__' :
    Main()