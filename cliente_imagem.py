# -*- coding: utf-8 -*-
import socket

# Crias um novo socket IPv4 + TCP
# Estes são os valores por defeito, portanto podes omitilos...
sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM)

# Tenta estabelecer a conexão.
# Aqui colocar o IP da maquina a que te queres conectar e a porta que
# colocas-te no programa servidor.
sock.connect( ("192.168.42.189", 65432) )
print( ">> Conexão estabelecida!" )

# Aqui alteras o nome e o directório consuate as necessidades
# Atenção ao modo que escolhes para abrir o ficheiro. Tens de utilizar
# modo binario: "wb"
f = open( "/home/leo/teste.jpg", "rb" )
# Variável para onde vai ser carregado o ficheiro.
data = ""
# Carrega para a variável 'data' cada linha do ficheiro.
# Atenção ao tamanho dos ficheiros e à memória livre
data = f.readlines()
for line in data:
    # Envia cada linha para o servidor.
    sock.send( line )

# Esta é a parte em que enviamos para o servidor a informação de que a
# imagem foi enviada na totalidade.
EOF = "\n\r##"
sock.send( EOF )
#
f.close()

# Muito importante fechar o socket criado.
sock.close()
