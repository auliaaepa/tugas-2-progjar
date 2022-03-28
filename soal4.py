import requests

# define URI
URI = "http://classroom.its.ac.id"

# make a HTTP request to the URI
r = requests.get(URI)

# get charset from server response to the HTTP request
charset = r.encoding
print(charset)

# close connection
r.close()