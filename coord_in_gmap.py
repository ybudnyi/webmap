import shelve
from selenium import webdriver
import os

# Only DB name, without extension
print(os.listdir())
db_name = input('Print name to chose db:\n--')


# Chose DB with markers coordinates for Google maps
def coord_from_shelve(name):
    with shelve.open(name) as db:
        for num, key in enumerate(db.keys()):
            print(f'{num + 1}) {key}')
        x = input('Print marker number wich you want to display:\n--')
        x = int(x) - 1
        l = list(db.keys())
        s = l[x]
        coord = db[s]
        return coord


# Send your coordinate to google maps
page = coord_from_shelve(db_name)
chrome_brw = webdriver.Chrome('.\\chromedriver')
chrome_brw.get('https://www.google.com.ua/maps/')
user_mess = chrome_brw.find_element_by_id("searchboxinput")
user_mess.clear()
user_mess.send_keys(page)
button = chrome_brw.find_element_by_class_name("searchbox-searchbutton")
button.click()

if __name__ == 'main':
    coord_from_shelve('home')
