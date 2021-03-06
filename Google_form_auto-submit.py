import subprocess

if(subprocess.run("pip3 show requests", stdout=subprocess.DEVNULL,
                  stderr=subprocess.DEVNULL).returncode == 1):
    print("Install the library need it for the script...")
    subprocess.run("pip3 install requests", stdout=subprocess.DEVNULL)
    

import requests
import re
from datetime import datetime
import os
import json
def check_form(req):
    return re.search("closedform", req.text) == None
def post():
    with open("info.json", 'r') as jason_file:
        data = json.load(jason_file)
        submission = data["data"]
        url = data['url']
        values = list(dict(data["data"]).values())
        name = values[0]
        email = values[1]
        status = values[2]
        print(f"{url=}\n{name=}\n{email=}\n{status=}")
        req = requests.get(url)
        if (check_form(req)):
            sent = requests.post(url, submission)
            if sent:
                print('Success  Code ' + str(sent.status_code))
                with open("Attendance.log", "a") as log:
                    now = datetime.now()
                    date = now.strftime("%d/%m/%Y %H:%M:%S")
                    log.writelines(f"{date} ok\n")
                    print(f"{date} ok\n")
            else:
                print('An error has occurred  Code ' + str(sent.status_code))
        else:
            print("The form is close now try again later")
def creatNewFile():
    # for SDA-E Cybersecurity Attendance form keep the url empty
    geturl = input(
        "Enter google form url you want to submit (keep it empty for the default value):\n")
    if geturl == "":
        url = "https://docs.google.com/forms/d/e/1FAIpQLSdDYw8ubu1Mhlab3FEEFyFxoTqNS7l9mwVYSgOfdBRsVCNsKg/formResponse"
    else:
        url = re.search("(.*docs.google.com/forms/d/e/.*)/.*", geturl)
        url = url.group(1)+"/formResponse"
    req = requests.get(url)
    if (check_form(req)):
        e = re.findall(
            "(?:\"|)(?:Name|Email|Status)(?: \",|\",)null,\d,\[\[([0-9]+)", req.text)
        entry_Name = e[0]
        entry_Email = e[1]
        entry_Status = e[2]
        name = input("Enter your name:\n")
        email = input("Enter your email:\n")
        json_data = {
            "url": url,
            "data": {
                f"entry.{entry_Name}": name,
                f"entry.{entry_Email}": email,
                f"entry.{entry_Status}": "Present"
            }
        }
        with open("info.json", "w") as jason_file:
            json.dump(json_data, jason_file)
        post()
    else:
        print("The form is close now try again later")
if(os.path.exists('info.json')):
    post()
else:
    print("info.json file not found creating new one...")
    creatNewFile()
os.system("pause")
