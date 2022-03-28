import requests

# define URI
URI = "http://its.ac.id"

# make a HTTP request to the URI
r = requests.get(URI)

# get content-encoding from server response header to the HTTP request
content_encoding = r.headers["Content-Encoding"]
print(content_encoding)

# close connection
r.close()