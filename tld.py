#! /usr/bin/env python3



import requests
import threading
import sys
import time
from bs4 import BeautifulSoup
import random


first_part = "" #fucking hell
tlds = open("stuff/tlds.txt", "r")
try:
    first_part = sys.argv[1]
    if first_part == "--random":
        words = list(open('stuff/words.txt'))
        while True:
            first_part = random.choice(words)
            first_part = first_part.strip()
            if input("like " + first_part + "? (y): ") == "y":
                break
except:
    print(f"Usage:\npython3 {sys.argv[0]} word         goes through word.com word.org word.net and so on")
    print(f"python3 {sys.argv[0]} --random     picks a random word from stuff/words.txt")

    first_part = input("word: ")
    #exit()








headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:144.0) Gecko/20100101 Firefox/144.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Sec-GPC': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Priority': 'u=0, i',

}

def check(tld):


    try:


        try:
            req = requests.get(f"https://{first_part}{tld}", headers=headers)
            result = "https"
        except:
            req = requests.get(f"https://{first_part}{tld}", headers=headers)
            result = "http"

        html = req.text.lower()
        start_index = html.find("<title>")
        end_index = html.find("</title>")

        if start_index != -1 and end_index != -1 and end_index > start_index:
            title = req.text[start_index + len("<title>"):end_index].strip()

        else:
            title = " "


        if title == " ":
            pass # i cant remember but i think i had something here before when i wanted to skip all that had no title, ill just leave it here


        #usual words in domains that are being sold, prints out as blue
        elif ("$" in html or "lander" in html) or ("cleanpeppermintblack" in html or "sale" in html):
            print(f"\033[0;34m{result}://{first_part}{tld}  [{title}]\033[0m")

            pass

        else:
            print("\033[92m"+result+"://" + first_part + tld + "[ " + title + "]\033[0m")
    except:
        pass



for tld in tlds:
    tld = tld.strip()
    while threading.active_count() >= 200:
        time.sleep(1)
    

    thread = threading.Thread(target=check, args=(tld,))
    thread.start()
    print(f"Trying: {first_part + tld}                          ", end="\r")
