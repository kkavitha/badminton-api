import mechanize
import cookielib

br = mechanize.Browser()
cj = cookielib.LWPCookieJar()
br.set_cookiejar(cj)
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)

r = br.open('http://www.booknplay.in')
html = r.read()
for f in br.forms():
    f.set_all_readonly(False)
br.select_form(nr=0)
form = br.form
form['data[Ground][area]'] = ['OMR / Thuraipakkam']
form['data[Ground][date]'] = '2017-10-28'
br.submit()
print br.response().read()




