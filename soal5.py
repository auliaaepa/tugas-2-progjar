import requests
from bs4 import BeautifulSoup

# define URI
URI = "http://classroom.its.ac.id"

# get content
r = requests.get(URI)
soup = BeautifulSoup(r.text, "html.parser")

# find all list in the navbar and display it
find_ls = soup.find("li", {"class": "dropdown nav-item"})
print(find_ls.get_text("\n\t", strip=True))

while True:
    find_ls = find_ls.find_next_sibling("li", "dropdown nav-item")
    if not find_ls:
        break
    print(find_ls.get_text("\n\t", strip=True))

# ls = [text for text in soup.find("ul", {"class": "navbar-nav h-100 wdm-custom-menus links"}).strings]
# print(ls)

# print(soup.find("ul", {"class": "navbar-nav h-100 wdm-custom-menus links"}).get_text().strip())
