import datetime
import re

import mechanicalsoup

from constants import slots as time_slots


def find_courts(browser, date, page):
    availability = []
    divs = page.soup.find_all('div', class_='booking_list')
    for div in divs:
        data = {}
        center_divs = div.find_all("div", class_="bl_info")
        for center_div in center_divs:
            print ("Fetch name of the court")
            court_name = center_div.a.strong.contents[0]
            data[court_name] = []
            court_view_slot_buttons = div.find_all("button", class_="view_slot")
            for court_view_slot_button in court_view_slot_buttons:
                print ("Fetch slot availability")
                value = court_view_slot_button["value"]
                url = "http://www.booknplay.in/grounds/booking_layout/" + value + "/" + date + "/1"
                r = browser.open(url)
                divs = r.soup.find_all("div", id="court_lists")
                courts = divs[0].find_all("a", href=re.compile(r'court_lists'))
                for court in courts:
                    court_availability = {}
                    court_id = court["href"][1:]
                    court_number = court.contents[0]
                    court_availability[court_number] = []
                    court_div = r.soup.find_all("div", id=court_id)
                    slots = court_div[0].find_all("td", class_="available single_slot")
                    print('Adding available slots for '+ court_number)
                    for slot in slots:
                        court_availability[court_number].append(time_slots[slot["value"][-2:]])
                    data[court_name].append(court_availability)
        availability.append(data)
    return availability


def submit_for_date(date, areas):
    for area in areas:
        browser, page = select_area(area, date)
        print ('Finding courts')
        return find_courts(browser, date, page)


def select_area(area, date):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open('http://www.booknplay.in')
    browser.select_form('#contact-formm')
    browser['data[Ground][date]'] = date
    browser['data[Ground][area]'] = area
    page = browser.submit_selected()
    return browser, page


def get_locations():
    br = mechanicalsoup.StatefulBrowser()
    r = br.open('http://www.booknplay.in')
    locations = []
    options = r.soup.find_all("select")[1].find_all("option")
    for option in options:
        locations.append(option["value"])
    return locations


def get_availability(areas, slots):
    date_formate = '%Y-%m-%d'
    today = datetime.date.today().strftime(date_formate)
    tomorrow = (datetime.date.today() + datetime.timedelta(days=1)).strftime(date_formate)
    day_after_tomorrow = (datetime.date.today() + datetime.timedelta(days=2)).strftime(date_formate)
    # submit_for_date(str(today))
    # submit_for_date(str(tomorrow))
    # areas = get_locations()
    return submit_for_date(str(day_after_tomorrow), areas)

# get_availability(["Thiruvanmiyur"], "")
# submit_for_date('2017-11-2',"")
# get_locations()
