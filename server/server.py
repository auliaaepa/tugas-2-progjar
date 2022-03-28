import socket
import select
from threading import Thread
import queue
from time import sleep
from random import randint
import sys

BUF_SIZE = 4096

class ProcessThread(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True
        self.q = queue.Queue()

    def add(self, data):
        self.q.put(data)

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            try:
                # block for 1 second
                value = self.q.get(block=True, timeout=1)
                process(value)
            except queue.Empty:
                sys.stdout.write('.')
                sys.stdout.flush()

        if not self.q.empty():
            print("Elements left in the queue:")
            while not self.q.empty():
                print(self.q.get())


t = ProcessThread()
t.start()


def process(value):
    """
    Implement this. Do something useful with the received data.
    """
    print(value)
    sleep(randint(1, 5))  # emulating processing time


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)             # Create a socket object
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    host = socket.gethostname()     # Get local machine name
    port = 5000                     # Reserve a port for your service.
    server_socket.bind((host, port))            # Bind to the port
    print("Listening on port {p}...".format(p=port))

    server_socket.listen(5)  # Now wait for client connection.
    while True:
        try:
            client_socket, client_address = server_socket.accept()
            ready = select.select([client_socket, ], [], [], 2)
            if ready[0]:
                data = client_socket.recv(BUF_SIZE)
                # print data
                t.add(data)
        except KeyboardInterrupt:
            print("Stop.")
            break
        except socket.error:
            print("Socket error!")
            break
    cleanup()


def cleanup():
    t.stop()
    t.join()


if __name__ == "__main__":
    main()