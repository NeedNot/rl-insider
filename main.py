import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from openpyxl import Workbook

pc = 1
ps4 = 2
xbox = 3
switch = 4

f = open('inventory.json')
inventory = json.load(f)["inventory"]

min = 0
max = 0
minus = 0
x = 0
z = 0
workbook = Workbook()
sheet = workbook.active
list_of_urls = []
list_of_names = []
list_of_paint = []
list_of_cost = []
list_of_amount = []

def get_url(url):
    print(url)
    return requests.get(url)

for i in range(len(inventory)):
    name = inventory[i]['name']
    paint = inventory[i]['paint']
    type = inventory[i]['slot']
    quality = inventory[i]['quality']
    amount = inventory[i]['amount']
    trade = inventory[i]['tradeable']
    bp = inventory[i]['blueprint_item']
    bp_cost = inventory[i]['blueprint_cost']

    blueprint_name = False

    if trade == 'true' and quality != 'Common':
        if bp != "":
            name = bp
            blueprint_name = True

        if name == 'Peregrine TT: Crisis':
            name = 'Peregrine Crisis'
        if name == 'Peregrine TT: Hoodbar':
            name = 'peregrine hoodbar'

        if name == 'Warp Wave' and type == 'Animated Decal':
            name = 'warp wave decal'
        if name == 'Warp Wave' and type == 'Trail':
            name = 'warp wave trail'

        if name == 'Toon Sketch' and type == 'Paint Finish':
            name = 'toon_sketch_paint_finish'
        if name == 'Toon Sketch' and type == 'Trail':
            name = 'toon sketch trail'
        if name == 'Toon Sketch' and type == 'Rocket Boost':
            name = 'toon sketch boost'

        if name == 'Glitch: Glitched':
            name = 'Glitch_wheels_Glitched'

        if name == 'Incantor' and type == 'Trail':
            name = 'Incantor trail'
        if name == 'Incantor' and type == 'Rocket Boost':
            name = 'Incantor boost'

        if name == 'Pixel Fire' and type == 'Player Banner':
            name = 'pixel_fire_banner'
        if name == 'Pixel Fire' and type == 'Rocket Boost':
            name = 'pixel fire boost'

        if name == 'Insidio: Sticker Bomb':
            name = 'Insidio: Sticker Bom'

        if name == 'Hydraul1K':
            name = 'Hydral1K'
        x += 1
        print(x)
        name_format = name.replace(' ', '_').replace('(', '').replace(')', '').replace(':', '').replace("'", "").replace('.', '').replace('-', '_')

        if paint == "none":
            paint_format = ""
        if paint == "Titanium White":
            paint_format = "white"
        if paint == "Black":
            paint_format = "black"
        if paint == "Grey":
            paint_format = "grey"
        if paint == "Crimson":
            paint_format = "crimson"
        if paint == "Pink":
            paint_format = "pink"
        if paint == "Cobalt":
            paint_format = "cobalt"
        if paint == "Sky Blue":
            paint_format = "sblue"
        if paint == "Burnt Sienna":
            paint_format = "sienna"
        if paint == "Saffron":
            paint_format = "saffron"
        if paint == "Lime":
            paint_format = "lime"
        if paint == "Forest Green":
            paint_format = "fgreen"
        if paint == "Orange":
            paint_format = "orange"
        if paint == "Purple":
            paint_format = "purple"
        if blueprint_name:
            name = "Blue print: "+name
        list_of_names.append(name)
        list_of_paint.append(paint)
        list_of_cost.append(bp_cost)
        list_of_amount.append(amount)

        list_of_urls.append(f"https://rl.insider.gg/en/pc/{name_format}/{paint_format}")

with ThreadPoolExecutor(max_workers=100) as pool:
    response_list = list(pool.map(get_url,list_of_urls))
runs = -1
print('ted')
for response in response_list:
    runs += 1
    bp_cost = list_of_cost[runs]
    amout = list_of_amounts[runs]
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="matrixRow0")
    print("L91", runs)
    try:
        price_elements = results.find_all("td")
        price = price_elements[pc].text
    except:
        print(list_of_urls[runs])
    try:
        value_m = price.split()[-1]
        if value_m == "k":
            multiple = 1000.0
        elif value_m == "m":
            multiple = 1000000.0
        else:
            multiple = 1.0
    except:
        print("L99", price)

    try:
        min_price = (float(price.split()[0]) * multiple) - bp_cost
        max_price = (float(price.split()[2]) * multiple) - bp_cost
    except:
        pass

    if 0 > min_price:
        print(min_price)
        min_price = 0
    if 0 > max_price:
        max_price = 0

    min += (min_price*float(amount))
    max += (max_price*float(amount))

    sheet[f"A{runs+1}"] = list_of_names[runs]
    sheet[f"B{runs+1}"] = list_of_paint[runs]
    sheet[f"C{runs + 1}"] = min_price
    sheet[f"D{runs + 1}"] = max_price
    sheet[f"E{runs + 1}"] = bp_cost
    sheet[f"F{runs + 1}"] = amount

    #print("L112", list_of_names[runs], list_of_paint[runs], min_price, max_price)


print(min, max)
workbook.save(filename="hello_world.xlsx")