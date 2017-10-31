import mechanicalsoup


def submit_for_date(date):
    browser = mechanicalsoup.StatefulBrowser()
    browser.open('http://www.booknplay.in')
    browser.select_form('#contact-formm')
    browser['data[Ground][date]'] = date
    browser.submit_selected()


def get_locations():
    br = mechanicalsoup.StatefulBrowser()
    r = br.open('http://www.booknplay.in')
    locations = []
    options = r.soup.find_all("select")[1].find_all("option")
    map(lambda x: locations.append(x["value"]), options)
    print locations



# submit_for_date('2017-11-2')
get_locations()