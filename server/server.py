import socket
import select
import threading
import queue
import os
import configparser
import mimetypes
import datetime
from wsgiref.handlers import format_date_time

RECV_BUF = 4096
BACKLOG = 5
CONF_FILE = "httpserver.conf"

class ServerResponseThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.running = True
        self.q = queue.Queue()

    def add(self, client_socket, request_header):
        """put tuple (client socket, request header) to queue"""
        self.q.put((client_socket, request_header))

    def stop(self):
        """stop server"""
        self.running = False

    def run(self):
        """respond to the client in the queue when server running"""
        while self.running:
            try:
                client_socket, request_header = self.q.get(block=True, timeout=1)
                self.send_response(client_socket, request_header)
            except queue.Empty:
                pass
    
    def send_response(self, client_socket, request_header):
        """send a response to client_socket based on request_header"""
        # get requested file name (URN)
        request_file = request_header.split("\r\n")[0].split()[1]
        if request_file[0] == "/":
            request_file = request_file[1:]
        
        response_header, response_content = "", ""
        filepath = "index.html" if request_file == "" or request_file == "index.html" \
            else os.path.join("dataset", request_file)

        if filepath == "index.html":
            # send response in the form of index.html if file exist
            if os.path.exists(filepath):
                with open(filepath, "rb") as file:
                    response_content = file.read()
                response_status = "200 OK"
                content_mime = "text/html"
                content_length = len(response_content)
                response_header = self.get_response_header(response_status, content_mime, content_length)
            # send response in the form of directory listing if file doesn't exist
            else:
                response_content = self.get_lisdir("").encode()
                response_status = "200 OK"
                content_mime = "text/html"
                content_length = len(response_content)
                response_header = self.get_response_header(response_status, content_mime, content_length)
        elif os.path.isdir(filepath):
            # send response in the form of directory listing
            response_content = self.get_lisdir(request_file).encode()
            response_status = "200 OK"
            content_mime = "text/html"
            content_length = len(response_content)
            response_header = self.get_response_header(response_status, content_mime, content_length)
        elif os.path.isfile(filepath):
            # send response in the form of file attachment
            with open(filepath, "rb") as file:
                response_content = file.read()
            response_status = "200 OK"
            content_mime = mimetypes.guess_type(filepath)[0]
            content_length = len(response_content)
            content_name = os.path.basename(filepath)
            response_header = self.get_response_header(response_status, content_mime, content_length, content_name)
        else:
            # send response in the form of 404.html if uri invalid
            filepath = "404.html"
            with open(filepath, "rb") as file:
                response_content = file.read()
            response_status = "404 Not Found"
            content_mime = "text/html"
            content_length = len(response_content)
            response_header = self.get_response_header(response_status, content_mime, content_length)
        
        # send response
        client_socket.sendall(response_header.encode()+response_content)
        print("SEND", client_socket.getpeername())

    def get_response_header(self, status, mime, length, filename=None):
        """generate response header"""
        response_header = "HTTP/1.0 " + status + "\r\n"
        response_header += "Content-Type: " + mime + "; charset=UTF-8\r\n"
        response_header += "Content-Length: " + str(length) + "\r\n"
        if filename:
            response_header += "Content-Disposition: attachment; filename=" + filename + "\r\n"
        response_header += "Date: " + format_date_time(datetime.datetime.utcnow().timestamp()) + "\r\n"
        response_header += "\r\n"
        return response_header

    def get_lisdir(self, root):
        """generate html file of directory listing"""
        response_content = """
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{title}</title>
        </head>
        <body>
            <h1>{title}</h1>
        """.format(title="Index of /"+root)
        
        path = "" if root == "" else "/"+root
        url = "http://" + host + ":" + str(port)
        for _, dirs, files in os.walk("dataset" + path):
            if path != "":
                response_content += """
                    <div><a href="{}">
                        ../
                    </a></div>
                """.format(url + os.path.dirname(path))
            for dirname in dirs:
                response_content += """
                    <div><a href="{}">
                        {}/
                    </a></div>
                """.format(url + path + "/" + dirname, dirname)
            for filename in files:
                response_content += """
                    <div><a href="{}">
                        {}
                    </a></div>
                """.format(url + path + "/" + filename, filename)
            break
        
        response_content += """
        </body>
        </html>
        """
        return response_content

# initialize ServerResponseThread object and start it
server_response = ServerResponseThread()
server_response.start()

# initialize socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# get port for "localhost" from config file and bind to it
config = configparser.ConfigParser()
config.read(CONF_FILE)
host = "localhost"
port = int(config[host]["Port"])
server_socket.bind((host, port))

# listen to client
server_socket.listen(BACKLOG)

while True:
    try:
        # print(threading.current_thread().name)
        # accept client
        client_socket, client_address = server_socket.accept()
        ready = select.select([client_socket, ], [], [], 2)
        if ready[0]:
            # receive request and send response to the valid request
            request_header = client_socket.recv(RECV_BUF).decode()
            if request_header != "":                
                print("RECV", ready[0][0].getpeername(), request_header.split("\r\n")[0])
                server_response.add(ready[0][0], request_header)

    except KeyboardInterrupt:
        print("Stop")
        break

    except socket.error:
        print("Socket error!")
        break

server_response.stop()
server_response.join()