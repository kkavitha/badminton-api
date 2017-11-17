import datetime
import re

import mechanicalsoup


def submit_for_date(date, areas):
    for area in areas:
        print(area)
        browser = mechanicalsoup.StatefulBrowser()
        browser.open('http://www.booknplay.in')
        browser.select_form('#contact-formm')
        browser['data[Ground][date]'] = date
        browser['data[Ground][area]'] = area
        page = browser.submit_selected()
        view_slots = page.soup.find_all("button", class_="view_slot")
        if len(view_slots) > 0:
            value = view_slots[0]["value"]
            url = "http://www.booknplay.in/grounds/booking_layout/" + value + "/" + date + "/1"
            r = browser.open(url)
            divs = r.soup.find_all("div", id="court_lists")
            courts = divs[0].find_all("a", href=re.compile(r'court_lists'))
            for court in courts:
                court_id = court["href"][1:]
                print court_id
                court_div = r.soup.find_all("div", id=court_id)
                slots = court_div[0].find_all("td", class_="available single_slot")
                for slot in slots:
                    print (slot["value"])


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
    areas = get_locations()
    submit_for_date(str(day_after_tomorrow), areas)


# submit_for_date('2017-11-2')
# get_locations()


