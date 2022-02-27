import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from openpyxl import Workbook
from tqdm import tqdm

pc = 1
ps4 = 2
xbox = 3
switch = 4

f = open('inventory.json')
inventory = json.load(f)["inventory"]

if input("Enable Blueprints? (y/n): ") == "y":
    bp_setting = True
else:
    bp_setting = False
if input("Enable Items? (y/n): ") == "y":
    item_setting = True
else:
    item_setting = False


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
    #print(url)
    #Counter.count()
    try:
        x = requests.get(url, timeout=10)
        if x == 'None':
            print('Null response')
            get_url(url)
        else:
            return x

    except:
        get_url(url)
# class Counter:
#     x = -1
#     def count():
#         Counter.x += 1
#         print(Counter.x)

def can_run(bp):
    if bp_setting == False and bp != "":
        return False
    if item_setting == False and bp == "":
        return False
    return True

for i in tqdm(range(len(inventory)), desc="Filtering eligible items"):
    name = inventory[i]['name']
    paint = inventory[i]['paint']
    type = inventory[i]['slot']
    quality = inventory[i]['quality']
    amount = inventory[i]['amount']
    trade = inventory[i]['tradeable']
    bp = inventory[i]['blueprint_item']
    bp_cost = inventory[i]['blueprint_cost']

    blueprint_name = False
    if trade == 'true' and quality != 'Common' and can_run(bp):
        if bp != "":
            name = bp
            blueprint_name = True

        if name == 'Peregrine TT: Crisis':
            name = 'Peregrine Crisis'
        if name == 'Peregrine TT: Hoodbar':
            name = 'peregrine hoodbar'

        if name == 'Invader' and quality == 'Common':
            name = 'Invader common'
        if name == 'Invader' and quality == 'Very Rare':
            name = 'Invader veryrare'
        if name == 'Invader' and quality == 'Exotic':
            name = 'Invader exotic'

        if name == 'Blade Wave':
            name = 'blade wave 2020 inverted'

        if name == 'Backfire: Cruster Buster':
            name = 'Cruster Buster'

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
        #print(x)
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
            name = "Blueprint: "+name
        list_of_names.append(name)
        list_of_paint.append(paint)
        list_of_cost.append(bp_cost)
        list_of_amount.append(amount)

        list_of_urls.append(f"https://rl.insider.gg/en/pc/{name_format}/{paint_format}")

with ThreadPoolExecutor(max_workers=10) as pool:
    response_list = list(tqdm(pool.map(get_url,list_of_urls), total=len(list_of_urls), desc="Downloading item details"))
runs = -1
error_list = []
#print('ted')
for response in tqdm(response_list, desc="Getting prices"):
    runs += 1
    bp_cost = list_of_cost[runs]
    amount = list_of_amount[runs]
    try:
        soup = BeautifulSoup(response.content, "html.parser")
        results = soup.find(id="matrixRow0")
    except:
        pass
        #print(response)
        #print("error", list_of_names[runs])
    #print("L91", runs)
    try:
        price_elements = results.find_all("td")
        price = price_elements[pc].text
    except:
        error_list.append(list_of_urls[runs])
    try:
        value_m = price.split()[-1]
        if value_m == "k":
            multiple = 1000.0
        elif value_m == "m":
            multiple = 1000000.0
        else:
            multiple = 1.0
        min_price = (float(price.split()[0]) * multiple) - bp_cost
        max_price = (float(price.split()[2]) * multiple) - bp_cost
    except:
        #print("L99", price)
        min_price = 0
        max_price = 0


    if 0 > min_price:
        #print(min_price)
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

    #print("L112", list_of_names[runs], list_of_paint[runs], min_price, max_price)

print("min:",min, "max:",max)
print("Item prices outputted to prices.xlsx")
print("The following links were unable to be downloaded. please report this to Need_Not so it can be fixed:")
for i in error_list:
    print(i)
sheet[f"C{runs + 2}"] = min
sheet[f"D{runs + 2}"] = max
workbook.save(filename="prices.xlsx")