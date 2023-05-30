import requests, os, json, csv, time, random, schedule
from datetime import datetime
from bs4 import BeautifulSoup


#change the current working directory 
new_directory = "c:/users/nelson/documents" 
os.chdir(new_directory)


url = 'https://mapleroyals.com/api/v1/get_status'

def get_player_count():
    #send a GET request to the website and parse the HTML content 
    response = requests.get(url, verify=False)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.content, 'html.parser')

    data = str((soup))

    #store the data into a json file 
    with open ('data.json', 'w') as f: 
        json.dump(data, f)

    #open the json file and retrive the player count 
    with open('data.json') as f: 
        data = json.load(f)
        data_dict = json.loads(data)

    return data_dict["onlineCount"]

def write_to_csv(player_count): 
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open('playercount.csv', 'a', newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerow([current_time, player_count])
        print("Player count of " + str(player_count) + " recorded at " + current_time)

def get_random_minute(start, end):
    return str(random.randint(start, end)).zfill(2)

def job():
    current_minute = int(datetime.now().strftime('%M'))
    if 0 <= current_minute <= 5 or 15 <= current_minute <= 20 or 30 <= current_minute <= 35 or 45 <= current_minute <= 50:
        write_to_csv(get_player_count())

schedule.every().hour.at(":" + get_random_minute(0, 5)).do(job)
schedule.every().hour.at(":" + get_random_minute(15, 20)).do(job)
schedule.every().hour.at(":" + get_random_minute(30, 35)).do(job)
schedule.every().hour.at(":" + get_random_minute(45, 50)).do(job)

while True:
    schedule.run_pending()
    time.sleep(30)
    