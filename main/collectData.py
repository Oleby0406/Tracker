import requests
import json
import schedule
import time
import subprocess

url = "https://library.ucsd.edu/assets/availability/data/labstats.php"

payload = ""
headers = {
    "authority": "waitz.io",
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9",
    "if-none-match": "W/^\^3dd-5yXTvCVLxTn6uvh/zE8RvVWdf7E^^",
    "origin": "https://recreation.ucsd.edu",
    "referer": "https://recreation.ucsd.edu/",
    "sec-ch-ua": "^\^Not.A/Brand^^;v=^\^8^^, ^\^Chromium^^;v=^\^114^^, ^\^Google",
    "sec-ch-ua-mobile": "?1",
    "sec-ch-ua-platform": "^\^Android^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Linux; Android 11; Pixel 5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.91 Mobile Safari/537.36"
}

dataArray = []
timeArray = ['12:00', '12:30', '13:00', '13:30', '14:00', '14:30', '15:00', '15:30', '16:00', '16:30', 
            '17:00', '17:30', '18:00', '18:30', '19:00', '19:30', '20:00', '20:30', '21:00']
response = requests.request("GET", url, data=payload, headers=headers)
data = json.loads(response.text)

f = open("main\static\libraryCollectedData.txt", "a")
f.write(str(time.ctime()) + "\n")

def getData():
    #one time check to even out lists if data is collected later than expected
    if len(dataArray) == 0:
        firstTimeCollected = str(time.ctime())[11:16]
        for i in timeArray:
            if i != firstTimeCollected:
                dataArray.append(-1)
            else:
                break
    response = requests.request("GET", url, data=payload, headers=headers)  
    data = json.loads(response.text)
    util = data[2]["utilization_availability"]
    #exit condition
    if data[2]["time_availability"]["availability_level"] != "open_now":
        schedule.clear()
        return schedule.CancelJob
    percentage = round((util["total_count"] - util["available_count"]) / util["total_count"], 2)
    dataArray.append(percentage)
    print(time.ctime())
    print(dataArray)

collectOne = schedule.every().hour.at(':00').do(getData)
collectTwo = schedule.every().hour.at(':30').do(getData)

try: 
    while True:
        schedule.run_pending()
        if (not schedule.jobs):
            break
        time.sleep(1)
except KeyboardInterrupt:
    pass

finally: 
    schedule.cancel_job(collectOne)
    schedule.cancel_job(collectTwo)
    while len(dataArray) < 19:
        dataArray.append(-1)
    f.write("[" + ', '.join(str(x) for x in dataArray) + "]" + "\n")
    f.write("[" + ', '.join(str(x) for x in timeArray) + "]" + "\n")
    f.write("\n")
    f.close()
    subprocess.run(["python", "analyze.py"])