'''
Author: Miles Catlett
Date: 7/22/2023
File: incendiary.py
This is another brewery. It's made with a wix site, so the events where just long strings. I had to do a lot of
work with the strings to extract the title and dates.
'''
from bs4 import BeautifulSoup
import requests
from datetime import datetime
from models import BeerFoodTruck


def incendiary():
    data = []
    out = []
    urls = [
        "https://www.incendiarybrewing.com/shows-events"
    ]
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        events = soup.findAll('div', attrs={"data-mesh-id": "comp-lfwpzkvlinlineContent"})
        for event in events:
            lines = event.text.split('\n')
            for line in lines:
                location = 'Incendiary - Lewisville'
                if True in [c.isdigit() for c in line] \
                        and 'Oyster 365' not in line \
                        and 'noon' not in line \
                        and '-' not in line \
                        and ',' not in line:
                    i = line.index(' ')
                    time = line[[c.isdigit() for c in line[i:-1]].index(True) + 3:len(line)].lstrip()
                    if line[line.index('pm')-1].isspace():
                        start = datetime.strptime(f"{line[0:i]}/{datetime.today().year} {time}", '%m/%d/%Y %I %p')
                    if not line[line.index('pm')-1].isspace():
                        start = datetime.strptime(f"{line[0:i]}/{datetime.today().year} {time}", '%m/%d/%Y %I%p')
                    end = datetime.strptime(f"{line[0:i]}/{datetime.today().year} 9 pm", '%m/%d/%Y %I %p')
                    truck = line[i+1:[c.isdigit() for c in line[i:-1]].index(True)+3].rstrip()
                    uid = 'incendiary ' + truck + str(start) + str(end)
                    data.append([location, truck, start, end, uid])
                elif True in [c.isdigit() for c in line] \
                        and 'Oyster 365' in line:
                    i = line.index(' ')
                    time = line[line.index('365') + 3:len(line)].lstrip()
                    if line[line.index('pm')-1].isspace():
                        start = datetime.strptime(f"{line[0:i]}/{datetime.today().year} {time}", '%m/%d/%Y %I %p')
                    if not line[line.index('pm')-1].isspace():
                        start = datetime.strptime(f"{line[0:i]}/{datetime.today().year} {time}", '%m/%d/%Y %I%p')
                    truck = line[i + 1:[c.isdigit() for c in line[i:-1]].index(True) + 3].rstrip()
                    uid = 'incendiary ' + truck + str(start) + str(end)
                    data.append([location, truck, start, end, uid])
                elif True in [c.isdigit() for c in line] \
                        and ', ' in line:
                    s = line.split(', ')
                    line = s[0]
                    date = f"{line[0:i]}/{datetime.today().year}"
                    first = s[0].replace(f"{line[0:i]} ", "")
                    s.pop(0)
                    s.insert(0, first)
                    for item in s:
                        time = item[[c.isdigit() for c in item].index(True):len(item)]
                        if not time[time.index('pm')-1].isspace() and '-' not in time:
                            start = datetime.strptime(f"{date} {time}", '%m/%d/%Y %I%p')
                        if time[time.index('pm')-1].isspace() and '-' not in time:
                            start = datetime.strptime(f"{date} {time}", '%m/%d/%Y %I %p')
                        if time[time.index('pm') - 1].isspace() and '-' in time:
                            string = time[time.index('-'):len(time)]
                            start = datetime.strptime(f"{date} {time.replace(string, '')}"
                                                      f" pm", '%m/%d/%Y %I %p')
                        if 'noon in item':
                            start = datetime.strptime(f"{date} 12 pm", '%m/%d/%Y %I %p')
                        truck = item.replace(time, '')
                        truck = truck.replace('noon-', '')
                        uid = 'incendiary ' + truck + str(start) + str(end)
                        data.append([location, truck, start, end, uid])
    u = BeerFoodTruck.query.all()
    u = [i.uid for i in u]
    for item in data:
        if item[4] not in u:
            out.append(
                BeerFoodTruck(
                    brewery=item[0],
                    food_truck=item[1],
                    start=item[2],
                    end=item[3],
                    uid=item[4]
                )
            )
    return out
