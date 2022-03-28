import requests

# define URI
URI = "http://its.ac.id"

# make a HTTP request to the URI
r = requests.get(URI)

# get status code and its reason from server response to the HTTP request
status_code = r.status_code
reason = r.reason
print(status_code, reason)

# close connection
r.close()