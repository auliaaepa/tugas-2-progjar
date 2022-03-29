import socket
import ssl
import re

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('www.its.ac.id', 443)
client_socket = ssl.wrap_socket(client_socket, keyfile=None, 
                certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, 
                ssl_version=ssl.PROTOCOL_SSLv23)
client_socket.connect(server_address)

request_header = ('GET / HTTP/1.1\r\nHost: www.its.ac.id\r\nConnection: close\r\nAccept: text/html\r\nAccept-Encoding: gzip, deflate, br\r\n\r\n').encode('utf-8')
client_socket.sendall(request_header)

response = b''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received

# print(response[:572].decode('utf-8'))
response_header = response[:572].decode('utf-8')
# response_header = response.split('\r\n\r\n')[0]
# print(response_header)

# no 1
string = response_header.split('\r\n')[0]
status_code = re.search(r'([1-5][0-9][0-9].*)', string).group(1)
print(status_code)

# no 2
encoding = re.search(r'\bContent-Encoding: (.*)\n\b', response_header).group(1)
print(encoding)

# no 3
protocol = re.search(r'(\b[A-Za-z0-9./]* \b)', string).group(1)
print(protocol)

client_socket.close()
