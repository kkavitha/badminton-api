import re

import mechanicalsoup

locations = {"Thoraipakkam": ['12.9416037', '80.23620959999994']
             # ,"Perungudi": ['12.9653652', '80.24610570000004']
             # ,"Thiruvanmyur": ['12.9830269', '80.2594001']
             # ,"Velachery": ['12.975971', '80.22120919999998']
             # ,"Adambakkam": ['12.9874863', '80.20459189999997']
             }
br = mechanicalsoup.StatefulBrowser()


def find_availability():
    free_slots = {}
    for location in locations:
        lat = locations[location][0]
        long = locations[location][1]
        json = 'https://www.booknplay.in/grounds/new_search/7/Chennai/' + lat + '/' + long + '/0/1000.json'
        r = br.open(json)
        find_venues_in_location(free_slots, r)
        print(free_slots)


def find_venues_in_location(free_slots, r):
    venues = r.soup.find_all("div", {"class": "content venue"})
    for venue in venues:
        courts_ = {}
        venue_name = find_venue_name(venue)
        free_slots[venue_name] = courts_
        link = venue.find("a")['href']
        r = br.open('https://www.booknplay.in/' + link)
        final_venues = r.soup.find_all("a", {"href": re.compile("users/login*")})
        for final_venue in final_venues:
            get_courts(final_venue, courts_)


def find_venue_name(venue):
    venue_name = venue.find("div", {"class": "venue-name"}).find("a").text
    return venue_name


def get_courts(final_venue, courts_):
    split_ = final_venue['href'].split("=")[1]
    r = br.open(split_)
    book_now_button = r.soup.find("div", {"id": re.compile("booknow*")})
    if book_now_button is not None:
        dates = {}
        venue_modal_id = book_now_button["data-id"]
        url = "https://www.booknplay.in/grounds/venue_modal/" + venue_modal_id + "/0"
        r = br.open(url)
        courts = r.soup.find("div", {"id": "div_court_list"}).find_all("a")
        court_number = 1
        for court in courts:
            courts_[court_number] = dates
            court_id = court["data-tab"]
            court_ = r.soup.find("div", {"data-tab": court_id})
            find_available_days(court_, court_id, dates)
            court_number += 1


def find_available_days(court_, court_id, dates):
    id_ = "date_" + court_id.split("_")[1] + "_"
    s = '{}*'.format(id_)
    days = court_.find_all("div", {"id": re.compile(s)})
    for day in days:
        find_available_slots_in_a_day(day, dates)


def find_available_slots_in_a_day(day, dates):
    date = day['id'].split("_")[2]
    venue_slots = []
    slot_row = day.find_all("div", {"class": "slot-row"})[3]
    slots = slot_row.find("div", {"class": "slot"})
    if slots is not None:
        for slot in slots:
            venue_slots.append(slot)
        dates[date] = venue_slots


find_availability()
