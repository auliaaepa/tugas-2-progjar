import http.client

# define URI
URI = "its.ac.id"

# connect to the server and make a request
conn = http.client.HTTPConnection(URI)
conn.request("GET", "/")

# get content-encoding from server response to the HTTP request
r = conn.getresponse()
version = r.version
if version == 11:
    print("HTTP/1.1")
elif version == 10:
    print("HTTP/1.0")
else:
    print(version)

# close connection
conn.close()