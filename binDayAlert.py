#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	Author: Lynsay A. Shepherd
	
	Date: December 2019

    File: binDayAlert.py

    License: MIT License (MIT)

	Description: Script to get bin collection dates and display them on ePaper screen
'''
#Imports required
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from inky import InkyPHAT
from lxml import html
from datetime import date
import requests


#Set the InkyPHAT type
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)

#Project fonts
font = ImageFont.truetype(FredokaOne, 22)
fontInfo = ImageFont.truetype(FredokaOne, 18)


#Request the bin webpage
def pullBinPage(binUrl):
	try:
		#Get the bin collection details for my address
		print ("Get the bin collection details for my address")
		page = requests.get(binUrl)
		print(page.status_code)

		if page.status_code == 200:
			parseBinData(page)
		else:
			print("Error")
	except:
		print "Error: "+str(e)


#Parse the content from the bin page
def parseBinData(binData):
	try:
		tree = html.fromstring(binData.content)

		#Get today's date
		today = date.today()
		todaysDate = today.strftime("%d/%m/%Y")

        #NOTE- you will need to edit the XPath expressions depending on the layout of your Council's webpage formatting
        #NOTE- modify the script to account for the various bins you may have collected e.g. refuse, recycling, garden waste, etc.

		#Get the listing for the first bin
		binOneType = ''.join(tree.xpath('//table/tr[2]/td[3]/text()'))
		binOneDate = ''.join(tree.xpath('//table/tr[2]/td[6]/text()'))

		#Get the listing for the second bin
		binTwoType = ''.join(tree.xpath('//table/tr[3]/td[3]/text()'))
		binTwoDate = ''.join(tree.xpath('//table/tr[3]/td[6]/text()'))

		#Striping the term "food waste" from the strings
		#Then strip "mixed" from "mixed recycling"
		toRemove = ' +'
		binOneType = binOneType.split(toRemove, 1)[0]
		binTwoType = binTwoType.split(toRemove, 1)[0]

		binOneType=binOneType.replace('Mixed ', '')
		binTwoType=binTwoType.replace('Mixed ', '')

		#Output
		todaysDateOutput = "Today: " + todaysDate
		binOneOutput = binOneType +": "+binOneDate
		binTwoOutput = binTwoType +": "+binTwoDate
		print(todaysDateOutput +", "+ binOneOutput +", "+binTwoOutput)
		outputBinDetails(todaysDateOutput, binOneOutput, binTwoOutput)

	except:
		print "Error: "+str(e)


#Request the bin webpage
def outputBinDetails(todaysDateOutput, binOneOutput, binTwoOutput):
	try:
		#Set a new screen drawing
		img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
		draw = ImageDraw.Draw(img)

		#Message to display and position
		w, h = font.getsize(todaysDateOutput)
		x = (inky_display.WIDTH / 2) - (w / 2)
		y = (inky_display.HEIGHT / 8) - (h / 8)

		#Draw the text on the screen
		draw.text((x, y), todaysDateOutput, inky_display.RED, font)
		draw.text((x, 50), binOneOutput, inky_display.BLACK, fontInfo)
		draw.text((x, 70), binTwoOutput, inky_display.BLACK, fontInfo)
		inky_display.set_image(img)
		inky_display.show()

	except:
		print "Error: "+str(e)




def main():
	try:
		print "Main method"
        #Note- add your local Council's bin collection page here
		theurl="#"
		pullBinPage(theurl)

		
	except Exception,e:
		print "Error: "+str(e)
    

if __name__ == "__main__":
    main()