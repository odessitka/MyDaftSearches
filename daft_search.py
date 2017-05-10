import urllib, re, sqlite3, googlemaps
from bs4 import BeautifulSoup
import dbhelpers
import HelperClasses
import webbrowser
import os

one_view = "oneview, blackrock"

def main():
    dbhelpers.initialize_db()
    extract_and_insert()
    calc_distances()
    filename = create_report()
    webbrowser.open_new_tab(filename)




def create_report():
    houses = dbhelpers.get_houses()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    f = open(dir_path + '\\report.html', 'w')
    message = compose_html(houses)
    f.write(message)
    f.close()
    filename = dir_path + '\\report.html'
    return filename


def calc_distances():
    addresses = dbhelpers.get_addresses()
    for (address, id) in addresses:
        matrix = HelperClasses.CommuteMatrix(address, one_view)
        dbhelpers.update_house(id, matrix.distance, matrix.duration, matrix.time_to_dart,
                               matrix.dart_sorting, matrix.near_by_dart)


def extract_and_insert():
    # Extract data from daft, clear it and insert into database
    for i in [1, 20, 40, 60, 80, 100]:
        url1 = "http://www.daft.ie/dublin-city/residential-property-for-rent/blackrock,booterstown,dun-laoghaire,monkstown,sandymount/?s%5Bmxp%5D=1850&s%5Badvanced%5D=1&rental_tab_name=advanced-sf&searchSource=rental"
        if i == 1:
            url = url1
        else:
            url = url1 + "&offset=" + str(i)
        html_of_search = urllib.request.urlopen(url).read()
        soup_of_search = BeautifulSoup(html_of_search, "lxml")
        boxes = soup_of_search.find_all('div', "box")
        if len(boxes) == 0: break
        for box in boxes:
            house = HelperClasses.House(box)
            dbhelpers.insert_house(house.price, house.address, house.url, house.image)


def compose_html(houses):
    message = """<html>
    <head></head>
    <body>
    <h1> Houses close to Oneview Healthcare </h1>
    <table border="1" width=93%>
    <colgroup>
        <col style="background-color:#E0F2F7">
        <col style="background-color:#F8E0EC">
        <col style="background-color:#E0F8E0">
        <col style="background-color:#F8E0EC">
        <col style="background-color:#E0F2F7">
    </colgroup>
    <tr><th>Time</th><th>Address</th><th>Price</th><th>Closest Dart</th><th>Walk to Dart</th></tr>"""
    for house in houses:
        message += "<tr><td>{a}</td><td><a href={d}>{b}</a></td><td>{c}</td><td>{e}</td><td>{f}</td><tr>".format(
            a=str(house[0]), b=house[1], c=house[2], d=house[3], e=house[4], f=house[5])
    message += """</table>
    </body>
    </html>"""
    return message


main()
