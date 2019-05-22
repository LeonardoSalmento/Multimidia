# -*- coding: utf-8 -*-
import socket, os, re, sys
from pkg_resources import load_entry_point

# Crias um novo socket TCP
# socket.AF_INET - IPv4
# socket.SOCK_STREAM - protocolo TCP
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )

# Associas o socket criado a um IP e uma porta.
# Neste caso ao IP de loopback e � porta 30000. � boa ideia escolher portas "altas"
# para evitar que a porta escolhida seja utilizada por aplica��es conhecidas.
# Portas de 0 a 1024 s�o reservadas. Portanto s�o de evitar.
# Se em vez de colocares um IP, deixares apenas "", o programa vai tentar
# "abrir" esta porta em todas as interfaces disponiveis.
sock.bind( ("0.0.0.0", 65432) )

# Metes o socket "� escuta". Ou seja, vai "abrir" a porta, e neste momento
# j� se consegue visualizar a porta "aberta"se fizeres uma listagem.
# O 1 indica quantas conex�es pode estar � espera de ser recebidas.
# Neste caso, apenas uma pode estar em espera. Todas as outras s�o descartadas.
sock.listen( 5 )

# Por fim fica � espera da primeira (e unica neste caso) liga��o.
# socket.accept() retorna uma tupla com o socket correspondente � liga��o
# e o endere�o remotodo e porta respectiva:
# Ex.: ( socket, ("IP_Remoto", Porta_Remota) )
s, clientSock = sock.accept()

print( ">> Conex�o recebida" )
print ( "IP Remoto: %s" % clientSock[0] )
print ( "Porta Remota: %d" % clientSock[1] )

# Vari�vel onde vai ser guardada a informa��o recebida
data = ""
# A string "\n\r##" � enviada pelo cliente no final da informa��o, ou seja,
# quando for recebida significa que toda a informa��o j� foi toda recebida.
# Enquanto n�o receber a string vai recebendo informa��o.
# O 1024 � o n�mero m�ximo de bytes que vai receber a cada leitura. Devido a
# este limite � necess�rio fazer v�rias leituras para receber uma imagem
# ou outro tipo de informa��o se for mais de 1024 bytes.
# O \n � encarado como apenas um caracter tal como o \r.
while ( data[-4:] != "\n\r##" ):    
    data += s.recv( 1024 )


cmd = "ping -c4 " + clientSock[0]
r = "".join(os.popen(cmd).readlines())
print r

# Retira-se a flag
data = data.replace( "\n\r##", "" )
# Aqui alteras o nome e o direct�rio consuate as necessidades
# Aten��o ao modo que escolhes para abrir o ficheiro. Tens de utilizar
# modo binario: "wb"
f = open( "/home/oi.jpg", "wb" )
f.write( data )
f.close()

# Muito importante fechar os sockets criados. Tanto o main como os
# resultates de conex�es recebidas.
sock.close()
s.close()
print( ">> Recep��o terminada!" )


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('pyspeedtest==1.2.7', 'console_scripts', 'pyspeedtest')()
    )
#exit(0)