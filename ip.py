import ipaddress
import requests
import threading
import time
from bs4 import BeautifulSoup


start_ip = input("First ip: ")
end_ip   = input("Second ip: ")
thread_amm = int(input("Thread ammount: "))
def run(ip):
    try:
        #print(f"requesting to http://{ip}")
        try:
            req = requests.get(f"https://{ip}", timeout=10)
            result = "https"
        except:
            req = requests.get(f"http://{ip}", timeout=10)
            result = "http"
        html = req.text.lower()
        start_index = html.find("<title>")
        end_index = html.find("</title>")
        if start_index != -1 and end_index != -1 and end_index > start_index:
            title = req.text[start_index + len("<title>"):end_index].strip()

        else:
            title = " "
        if "login" in html or "password" in html: #to avoid routers and camera logins
            print(f"\033[0;34m{result}://{ip} [{title}\033[0m")
        else:
            print(f"\033[92m{result}://{ip} [{title}]\033[0m")
    except Exception as e:
        pass


# Validate IP addresses
try:
    start = ipaddress.IPv4Address(start_ip)
    end = ipaddress.IPv4Address(end_ip)
except ipaddress.AddressValueError:
    raise ValueError("Invalid IP address supplied")

# Make sure start_ip <= end_ip
if start > end:
    raise ValueError("Starting IP must be less than or equal to ending IP")

# Loop through the range
for ip_int in range(int(start), int(end) + 1):
    while threading.active_count() > thread_amm:
        time.sleep(1)
    
    time.sleep(0.01)
    ip_str = str(ipaddress.IPv4Address(ip_int))
    thread = threading.Thread(target=run, args=(ip_str,))
    thread.start()
    print(f"Trying: {ip_str}                          ", end="\r")
