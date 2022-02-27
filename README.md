# rl-insider

this python script will total up the value of all your items in your inventory.

How to use:
download and install this bakkes mod plugin https://bakkesplugins.com/plugins/view/155
then export it to json and put that json file in the same folder as the py file. 

it will then export a spreadsheet with every item and every price along with a total price.

other features:
  only value blueprints
  only value items
  value both at once
  
coming soon:
  filter out rarities
  
issues:
  because this script is so early in the making it has a problem. and that is it gets rl insider urls by assuming that the url for a given item
  is the name with all special characters replaced with either an _ or nothing. however a few items such as pixel fire which is both a banner and a boost so the url contains a boost or banner in it.
  items like these are being found and fixed but it's not possible to know all of them so the script will tell you if it finds any. and if it does please send them to me so i can fix it
