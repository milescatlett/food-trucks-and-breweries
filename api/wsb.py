'''
Author: Miles Catlett
Date: 7/22/2023
File: wsb.py
This was by far the most difficulty I had. Using Selenium was very challenging. I tried to run this app on Ubuntu,
VPS hosting, and Windows. Unfortunately, I could only get it to run reliably on Windows. I played with Firefox,
Opera, and Chrome.
'''
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from models import BeerFoodTruck


def wmb():
    '''
    This is the first of two scripts. This one clicks on the next button and gets the events from next month.
    :return: database objects
    '''
    # These arguments are important for attempting to get Selenium to run on Ubuntu, and I didn't bother to remove
    # them for windows even though I don't need them. The scripts are running and a home server so I don't even need
    # run them in headless mode.
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # binary_path = '/usr/bin/chromedriver'
    # driver = webdriver.Chrome(service=Service(binary_path), options=options)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    # This calendar has pop-up events so Selenium was the only way to get the data.
    driver.get("https://plugin.eventscalendar.co/widget.html?pageId=rnzr4&compId=comp-jg2l6cob&viewerCompId=comp-jg2l6cob&siteRevision=69&viewMode=site&deviceType=desktop&locale=en&tz=America%2FNew_York&regionalLanguage=en&width=980&height=600&instance=bplNgPqFrXD115kQsFCdssYajjSx_ICEYK4iJPImA7E.eyJpbnN0YW5jZUlkIjoiMTA3MzVhYzAtYjNjOS00YzZhLTg2M2QtMzkxMThiMmQ0MWNiIiwiYXBwRGVmSWQiOiIxMzNiYjExZS1iM2RiLTdlM2ItNDliYy04YWExNmFmNzJjYWMiLCJzaWduRGF0ZSI6IjIwMjItMTItMDNUMTY6NDA6MDguMTM0WiIsInZlbmRvclByb2R1Y3RJZCI6InByZW1pdW0iLCJkZW1vTW9kZSI6ZmFsc2UsIm9yaWdpbkluc3RhbmNlSWQiOiI2MDNkODcyNi1hM2I3LTQ2YWItOTkzYi1hMzM0YjFmZTJmODIiLCJhaWQiOiI3MGU1OWNmNC00YzhjLTQ5NmItOGZhMC1kODU5MTFkZWQxY2UiLCJzaXRlT3duZXJJZCI6IjMxNDkwNGM4LTZkNWYtNGRiMS1hNzM2LTE4MDM5MmE5OGJmYiJ9&currency=USD&currentCurrency=USD&commonConfig=%7B%22brand%22:%22wix%22,%22bsi%22:%22adcc5aaf-81a9-4ade-94cb-da0ce6aa4115%7C2%22,%22BSI%22:%22adcc5aaf-81a9-4ade-94cb-da0ce6aa4115%7C2%22%7D&vsi=f03ef16b-a661-4171-9516-1f4fb446a770")
    title = driver.title
    time.sleep(10)
    driver.implicitly_wait(60)
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, value=" ")
    event_list = []
    for link in links:
        link.click()
        events = driver.find_elements(by=By.CLASS_NAME, value="popup-body")
        time.sleep(0.02)
        for event in events:
            event = event.text.split("\n")
            if len(event) > 1 and event[1] == 'close':
                more = driver.find_elements(by=By.CLASS_NAME, value="events-list")
                for items in more:
                    items = items.text.split("\n")
                    for i in range(0, len(items), 2):
                        date_split = items[i + 1]
                        date_split = date_split.rsplit(", ", 1)
                        # I had to add a lot of conditions here to single out the food trucks because the wise mans
                        # calendar has everything in one place.
                        if "Open" not in items[i] \
                                and "Vinyl" not in items[i] \
                                and "$" not in items[i] \
                                and "USA" not in items[i] \
                                and "Trivia" not in items[i] \
                                and "Music" not in items[i] \
                                and "Party" not in items[i] \
                                and "Boulder" not in items[i] \
                                and "Bimmers" not in items[i] \
                                and "Game" not in items[i] \
                                and "Books" not in items[i] \
                                and "Run" not in items[i] \
                                and "TICKETED" not in items[i] \
                                and "Wheel" not in items[i] \
                                and "WFDD" not in items[i] \
                                and "Play" not in items[i] \
                                and "Blood Drive" not in items[i] \
                                and "First Friday" not in items[i] \
                                and len(event) == 4:
                            event_list.append([items[i], date_split[0], date_split[1]])
            if len(event) > 1 and event[1] != 'close':
                if "Open" not in event[1] \
                        and "Vinyl" not in event[1] \
                        and "$" not in event[1] \
                        and "USA" not in event[1] \
                        and "Trivia" not in event[1] \
                        and "Music" not in event[1] \
                        and "Party" not in event[1] \
                        and "Boulder" not in event[1] \
                        and "Bimmers" not in event[1] \
                        and "Game" not in event[1] \
                        and "Books" not in event[1] \
                        and "Run" not in event[1] \
                        and "TICKETED" not in event[1] \
                        and "Wheel" not in event[1] \
                        and "WFDD" not in event[1] \
                        and "Play" not in event[1] \
                        and "Blood Drive" not in event[1] \
                        and "First Friday" not in event[1] \
                        and len(event) == 4:
                    event_list.append([event[1], event[2], event[3]])
        driver.find_element(by=By.CLASS_NAME, value="popup-close").click()
        time.sleep(0.02)
    sql = []
    eid = 0
    for event in event_list:
        eid += 1
        times = event[2].split('-')
        start_time = times[0]
        start_date = event[1] + ' ' + start_time
        end_date = ''
        if len(times) > 1:
            end_time = times[1]
            end_date = event[1] + ' ' + end_time
        brewery = "Wise Man Brewing"
        food_truck = event[0].replace("'", "")
        start = datetime.strptime(start_date, '%A, %B %d, %Y %I:%M%p')
        if end_date != '':
            end = datetime.strptime(end_date, '%A, %B %d, %Y %I:%M%p')
        else:
            end = ''
        uid = "wmb"+food_truck+start.strftime("%m/%d/%Y %H:%M:%S")+end.strftime("%m/%d/%Y %H:%M:%S")
        # By querying the uids I can check to make sure the event doesn't already exist in the database.
        u = BeerFoodTruck.query.all()
        u = [i.uid for i in u]
        if uid not in u and start > datetime.now():
            sql.append(
                BeerFoodTruck(
                    brewery=brewery,
                    food_truck=food_truck,
                    start=start,
                    end=end,
                    uid=uid
                )
            )
        # sql += f"{brewery}#{food_truck}#{str(start)}#{str(end)}#{uid}#{str(eid)}@"
    # f = open("wmb.txt", "w")
    # f.write(str(sql))
    # f.close()
    driver.close()
    driver.quit()
    return sql


def wmb_next():
    '''
    This is the second script. It's the same as the first. I was being kind of lazy here, and the only difference is
    really that we are not clicking on the next button to get next month's events.
    :return: database objects
    '''
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    # binary_path = '/usr/bin/chromedriver'
    # driver = webdriver.Chrome(service=Service(binary_path), options=options)
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get("https://plugin.eventscalendar.co/widget.html?pageId=rnzr4&compId=comp-jg2l6cob&viewerCompId=comp-jg2l6cob&siteRevision=69&viewMode=site&deviceType=desktop&locale=en&tz=America%2FNew_York&regionalLanguage=en&width=980&height=600&instance=bplNgPqFrXD115kQsFCdssYajjSx_ICEYK4iJPImA7E.eyJpbnN0YW5jZUlkIjoiMTA3MzVhYzAtYjNjOS00YzZhLTg2M2QtMzkxMThiMmQ0MWNiIiwiYXBwRGVmSWQiOiIxMzNiYjExZS1iM2RiLTdlM2ItNDliYy04YWExNmFmNzJjYWMiLCJzaWduRGF0ZSI6IjIwMjItMTItMDNUMTY6NDA6MDguMTM0WiIsInZlbmRvclByb2R1Y3RJZCI6InByZW1pdW0iLCJkZW1vTW9kZSI6ZmFsc2UsIm9yaWdpbkluc3RhbmNlSWQiOiI2MDNkODcyNi1hM2I3LTQ2YWItOTkzYi1hMzM0YjFmZTJmODIiLCJhaWQiOiI3MGU1OWNmNC00YzhjLTQ5NmItOGZhMC1kODU5MTFkZWQxY2UiLCJzaXRlT3duZXJJZCI6IjMxNDkwNGM4LTZkNWYtNGRiMS1hNzM2LTE4MDM5MmE5OGJmYiJ9&currency=USD&currentCurrency=USD&commonConfig=%7B%22brand%22:%22wix%22,%22bsi%22:%22adcc5aaf-81a9-4ade-94cb-da0ce6aa4115%7C2%22,%22BSI%22:%22adcc5aaf-81a9-4ade-94cb-da0ce6aa4115%7C2%22%7D&vsi=f03ef16b-a661-4171-9516-1f4fb446a770")
    title = driver.title
    time.sleep(10)
    driver.find_element(By.CLASS_NAME, "icon-arrow-right").click()
    time.sleep(10)
    driver.implicitly_wait(60)
    links = driver.find_elements(By.PARTIAL_LINK_TEXT, value=" ")
    event_list = []
    for link in links:
        link.click()
        events = driver.find_elements(by=By.CLASS_NAME, value="popup-body")
        time.sleep(0.02)
        for event in events:
            event = event.text.split("\n")
            if len(event) > 1 and event[1] == 'close':
                more = driver.find_elements(by=By.CLASS_NAME, value="events-list")
                for items in more:
                    items = items.text.split("\n")
                    for i in range(0, len(items), 2):
                        date_split = items[i + 1]
                        date_split = date_split.rsplit(", ", 1)
                        if "Open" not in items[i] \
                                and "Vinyl" not in items[i] \
                                and "$" not in items[i] \
                                and "USA" not in items[i] \
                                and "Trivia" not in items[i] \
                                and "Music" not in items[i] \
                                and "Party" not in items[i] \
                                and "Boulder" not in items[i] \
                                and "Bimmers" not in items[i] \
                                and "Game" not in items[i] \
                                and "Books" not in items[i] \
                                and "Run" not in items[i] \
                                and "TICKETED" not in items[i] \
                                and "Wheel" not in items[i] \
                                and "WFDD" not in items[i] \
                                and "Play" not in items[i] \
                                and "Blood Drive" not in items[i] \
                                and "First Friday" not in items[i] \
                                and len(event) == 4:
                            event_list.append([items[i], date_split[0], date_split[1]])
            if len(event) > 1 and event[1] != 'close':
                if "Open" not in event[1] \
                        and "Vinyl" not in event[1] \
                        and "$" not in event[1] \
                        and "USA" not in event[1] \
                        and "Trivia" not in event[1] \
                        and "Music" not in event[1] \
                        and "Party" not in event[1] \
                        and "Boulder" not in event[1] \
                        and "Bimmers" not in event[1] \
                        and "Game" not in event[1] \
                        and "Books" not in event[1] \
                        and "Run" not in event[1] \
                        and "TICKETED" not in event[1] \
                        and "Wheel" not in event[1] \
                        and "WFDD" not in event[1] \
                        and "Play" not in event[1] \
                        and "Blood Drive" not in event[1] \
                        and "First Friday" not in event[1] \
                        and len(event) == 4:
                    event_list.append([event[1], event[2], event[3]])
        driver.find_element(by=By.CLASS_NAME, value="popup-close").click()
        time.sleep(0.02)
    sql = []
    eid = 0
    for event in event_list:
        eid += 1
        times = event[2].split('-')
        start_time = times[0]
        start_date = event[1] + ' ' + start_time
        end_date = ''
        if len(times) > 1:
            end_time = times[1]
            end_date = event[1] + ' ' + end_time
        brewery = "Wise Man Brewing"
        food_truck = event[0].replace("'", "")
        start = datetime.strptime(start_date, '%A, %B %d, %Y %I:%M%p')
        if end_date != '':
            end = datetime.strptime(end_date, '%A, %B %d, %Y %I:%M%p')
        else:
            end = ''
        uid = "wmb"+food_truck+start.strftime("%m/%d/%Y %H:%M:%S")+end.strftime("%m/%d/%Y %H:%M:%S")
        u = BeerFoodTruck.query.all()
        u = [i.uid for i in u]
        if uid not in u and start > datetime.now():
            sql.append(
                BeerFoodTruck(
                    brewery=brewery,
                    food_truck=food_truck,
                    start=start,
                    end=end,
                    uid=uid
                )
            )
        # sql += f"{brewery}#{food_truck}#{str(start)}#{str(end)}#{uid}#{str(eid)}@"
    # f = open("wmb.txt", "w")
    # f.write(str(sql))
    # f.close()
    driver.close()
    driver.quit()
    return sql