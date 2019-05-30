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


    nomeArquivo = input("Qual o nome do arquivo? -> ").encode()
    if nomeArquivo != 'q'.encode():
        s.send(nomeArquivo)
        data = s.recv(1024)
        if data[:6] == 'EXISTS'.encode():
            tamanhoArquivo = int(data[6:].decode())
            mensagem = input("O arquivo possui tamanho = " + str(tamanhoArquivo) +"Bytes, Deseja enviar? (S/N)? -> ")
            if mensagem == 'S':
                s.send("OK".encode())
                f = open('new_'+nomeArquivo.decode(), 'wb')
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < tamanhoArquivo:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv/float(tamanhoArquivo))*100)+ "% Done", end='\r')
                print("Arquivo Enviado!")
                f.close()
        else:
            print ("Arquivo não existe!")

    s.close()

def transferenciaUdp():
    porta = 5001

    server = (host,5000)

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    nomeArquivo = input("Qual o nome do arquivo? -> ").encode()
    if nomeArquivo != 'q'.encode():
        s.sendto(nomeArquivo,server)
        data, addr = s.recvfrom(1024)
        if data[:6] == 'EXISTS'.encode():
            tamanhoArquivo = int(data[6:].decode())
            mensagem = input("O arquivo possui tamanho = " + str(tamanhoArquivo) +"Bytes, Deseja enviar? (S/N)? -> ")
            if mensagem == 'S':
                s.sendto("OK".encode(), addr)
                f = open('new_'+nomeArquivo.decode(), 'wb')
                data, addr = s.recvfrom(1024)
                totalRecv = len(data)
                f.write(data)
                while totalRecv < tamanhoArquivo:
                    data, addr = s.recvfrom(1024)
                    totalRecv += len(data)
                    f.write(data)
                    print("{0:.2f}".format((totalRecv/float(tamanhoArquivo))*100)+ "% Done", end='\r')
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
    tempoEnvio = (end-begin)
    velocidadeTransferencia = 8/tempoEnvio

    print("A taxa de transferencia da rede %.2f"  % velocidadeTransferencia)

    if velocidadeTransferencia>100:
        print("A melhor opção, é utilizar o TCP")
        transferenciaTcp()
    else:
        print("A melhor opção é utilizar o UDP")
        transferenciaUdp()


def ping():
    cmd = "ping -c4 " + host
    r = "".join(os.popen(cmd).readlines())
    print (r)


def Main():
    taxaTransferencia('127.0.0.1',6000)
    ping()




if __name__ == '__main__' :
    Main()