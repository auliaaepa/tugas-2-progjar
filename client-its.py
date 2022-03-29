import socket
import ssl
import re

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('its.ac.id', 443)
client_socket.connect(server_address)
client_socket = ssl.wrap_socket(client_socket, keyfile=None, 
                certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, 
                ssl_version=ssl.PROTOCOL_SSLv23)

request_header = b"GET https://www.its.ac.id/ HTTP/1.1\r\nHost: its.ac.id\r\nConnection: close\r\n\r\n"
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')

# print(response)
response_header = response.split('\r\n\r\n')[0]
print(response_header)

# no 1
string = response_header.split('\r\n')[0]
status_code = re.search(r'([1-5][0-9][0-9].*)', string).group(1)
print(status_code)

# no 3
protocol = re.search(r'(\b[A-Za-z0-9./]* \b)', string).group(1)
print(protocol)

client_socket.close()
