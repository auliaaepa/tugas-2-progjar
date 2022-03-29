import socket
import ssl
import re
from bs4 import BeautifulSoup

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('classroom.its.ac.id', 443)
client_socket.connect(server_address)
client_socket = ssl.wrap_socket(client_socket, keyfile=None, 
                certfile=None, server_side=False, cert_reqs=ssl.CERT_NONE, 
                ssl_version=ssl.PROTOCOL_SSLv23)

request_header = b"GET https://classroom.its.ac.id/ HTTP/1.1\r\nHost: classroom.its.ac.id\r\nConnection: close\r\n\r\n"
client_socket.send(request_header)

response = ''
while True:
    received = client_socket.recv(1024)
    if not received:
        break
    response += received.decode('utf-8')

# print(response)
response_header = response.split('\r\n\r\n')[0]
# print(response_header)

# no 4
charset = re.search(r'\bcharset=(.*)\n\b', response_header).group(1)
print(charset)

# no 5
soup = BeautifulSoup(response, "html.parser")

# find all list in the navbar and display it
find_ls = soup.find("li", {"class": "dropdown nav-item"})
print(find_ls.get_text("\n\t", strip=True))

while True:
    find_ls = find_ls.find_next_sibling("li", "dropdown nav-item")
    if not find_ls:
        break
    print(find_ls.get_text("\n\t", strip=True))

client_socket.close()