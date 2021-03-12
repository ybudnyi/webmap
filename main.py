import folium
import os
import pyperclip
import pandas
import shelve
from selenium import webdriver

# Go to work folder
os.chdir('D:\\Py_Proj\\webmap')
directory = os.getcwd()
print(f'Your html page is in {directory} ')
north = ''
east = ''


# Get coordinates for base map
def get_cord():
    global north
    global east
    c = ''.join(list(pyperclip.paste()))
    cord = c.split(',')
    if len(cord) == 2:
        for i in cord:
            print(f'Your cordinates are = {i}')
    else:
        raise Exception

    north = cord[0]
    east = cord[1]


# Use only digit for Ctr+C
try:
    get_cord()
except Exception:
    print(f'Something wrong with your cordinates {north}, {east}. Must contain only numbers')
my_map = folium.Map(location=[north, east], zoom_start=12)


def markers_map():
    q_for_dict = ''
    sh = shelve.open(db_name)
    while q_for_dict.lower() != 'exit':
        k = input('Input markers name\n')
        c = input('Copy cordinates here')
        v = ''.join(list(c))
        x = v.split(',')
        marker_colect[k] = x
        q_for_dict = input('Press enter to continue or print exit:')
        sh[k] = x
    sh.close()


# Chose file from directory
def file_from_dir():
    print(f'Put your file with markers to the folder{directory}')
    d = os.listdir()
    for dig, dd in enumerate(d):
        print(f'{dig + 1}) {dd}')
    dm = input('Chose the digit of file you want to upload')
    dm = int(dm)
    chose = dm - 1
    files = d[chose]
    return files


# Uploads file with data for your marker layer(only csv, txt)
def upload_markers(fnc):
    # fg = folium.FeatureGroup(name='my_map')
    print(f'Read {fnc}')
    data = pandas.read_csv(fnc)
    lat = list(data['LAT'])
    lon = list(data['LON'])
    elev = list(data['ELEV'])

    def color_chose(x):  # For change colors of markers

        if int(x) < 2000:
            x = 'green'
        elif int(x) > 2400:
            x = 'red'
        else:
            x = 'orange'
        return x

    col = list(map(lambda x: color_chose(x), elev))

    for la, lo, el, co in zip(lat, lon, elev, col):
        x.add_child(folium.Marker(location=[la, lo], popup=str(el), icon=folium.Icon(color=co)))
        # my_map.add_child(fg)


q = input('If you want to load your markers from file print "1" or press enter to print them by hand\n--')
if q == '1':
    x = folium.FeatureGroup(name='my_map')
    upload_markers(file_from_dir())
    my_map.add_child(x)
# Make markers from your dictionary
else:
    marker_colect = {}
    db_name = input('Print name of DB to save your coordinates in:\n--')
    markers_map()
    fg = folium.FeatureGroup(name='my_map')
    for key_dict, cordinat in marker_colect.items():
        expl = input(f'If you want to describe your marker {key_dict}, please print here\n--:')
        col_chose = input('''Chose a color for your market
        -Red
        -Orange
        -Green\n--:''')
        x = folium.FeatureGroup(name='my_map')
        x.add_child(folium.Marker(location=cordinat, popup=expl, icon=folium.Icon(color=col_chose.lower())))
        my_map.add_child(x)
        print(f'Created marker for: {key_dict}')
        print('=' * 30 + 'Markers putted' + '=' * 30)

my_map.save('map.html')
coord_display = input('Do you want to see your markers on Google Map?')
if coord_display.lower() == 'yes':
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


    page = coord_from_shelve(db_name)
    chrome_brw = webdriver.Chrome('.\\chromedriver')
    chrome_brw.get('https://www.google.com.ua/maps/')
    user_mess = chrome_brw.find_element_by_id("searchboxinput")
    user_mess.clear()
    user_mess.send_keys(page)
    button = chrome_brw.find_element_by_class_name("searchbox-searchbutton")
    button.click()
