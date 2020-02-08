#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
	Author: Lynsay A. Shepherd
	
	Date: 14th December 2019

	Revised: 8th February 2020

	Desc: Script to get bin collection dates and display them on ePaper screen
'''

#Imports required
from PIL import Image, ImageFont, ImageDraw
from inky import InkyPHAT
from lxml import html
from datetime import date, timedelta
import datetime
import requests
import nexmo
import calendar


#Set the InkyPHAT type
inky_display = InkyPHAT("red")
inky_display.set_border(inky_display.WHITE)

#Project fonts - Roboto
font = ImageFont.truetype("Roboto-Bold.ttf", 22)
fontInfo = ImageFont.truetype("Roboto-Bold.ttf", 18)
fontUpdated = ImageFont.truetype("Roboto-Regular.ttf", 10)

#Setup the text messaging service
client = nexmo.Client(key='INSERT_KEY', secret='INSERT_SECRET')


#Request the bin webpage
def pullBinPage(binUrl):
	try:
		#Get the bin collection details for my address
		print ("Get the bin collection details for my address")
		page = requests.get(binUrl)
		print (page.status_code)

		if page.status_code == 200:
			parseBinData(page)
		else:
			print("oh")
	except:
		print ("Error getting page")


#Parse the content from the bin page
def parseBinData(binData):
	try:
		tree = html.fromstring(binData.content)

		#Get today's date
		today = date.today()
		todaysDate = today.strftime("%d/%m/%Y")

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


		#Output to terminal
		if binOneDate < binTwoDate:
			print ("The next bin to be emptied is " + binOneType + " on " + binOneDate)
			binOneOutput = binOneType +": "+binOneDate+"*"
			binTwoOutput = binTwoType +": "+binTwoDate
		
		else:
			print ("The next bin to be emptied is " + binTwoType + " on " + binTwoDate)
			binOneOutput = binOneType +": "+binOneDate
			binTwoOutput = binTwoType +": "+binTwoDate+"*"


		todaysDateOutput = "Today: " + todaysDate
		print(todaysDateOutput +", "+ binOneOutput +", "+binTwoOutput)

		#Print out bin details on the ePaper screen
		outputBinDetails(todaysDateOutput, binOneOutput, binTwoOutput)

		#Check if it's time to send a reminder SMS
		checkTextMessage(todaysDateOutput, binOneType, binOneDate, binTwoType, binTwoDate)

	except:
		print ("Error pulling bin data")



#Request the bin webpage
def checkTextMessage(todaysDateOutput, binOneType, binOneDate, binTwoType, binTwoDate):
	try:
		print ("Check text message")

		#Convert date strings to objects
		binOneDateObj = datetime.datetime.strptime(binOneDate, '%d/%m/%Y')
		binTwoDateObj = datetime.datetime.strptime(binTwoDate, '%d/%m/%Y')
		currentDate = date.today()

		#Text for SMS message
		if binOneDate < binTwoDate:
			textContent="Hi Lynsay, the next bin to be emptied is your " + binOneType + " bin on " + binOneDate

		else:
			textContent="Hi Lynsay, the next bin to be emptied is your" + binTwoType + " bin on " + binTwoDate


		#if it's the day before a bin is emptied, send a text
		if binOneDateObj.date()-timedelta(1) == currentDate:
			print (binOneDateObj.date()-timedelta(1))
			#Send message
			client.send_message({
				'from': 'BinDayAlert',
				'to': 'YOUR_PHONENUMBER',
				'text': textContent})
		

		elif binTwoDateObj.date()-timedelta(1) == currentDate:
			print (binTwoDateObj.date()-timedelta(1))
			#Send message
			client.send_message({
				'from': 'BinDayAlert',
				'to': 'YOUR_PHONENUMBER',
				'text': textContent})

	except:
		print ("Error handling text message")



#Request the bin webpage
def outputBinDetails(todaysDateOutput, binOneOutput, binTwoOutput):
	try:
		#Time updated printed to screen
		x = datetime.datetime.now()
		print(x.strftime("%d/%m/%Y %H:%M:%S"))
		lastUpdated=x.strftime("%d/%m/%Y %H:%M:%S")
		lastUpdatedString="[Updated:" + lastUpdated + "]"

		#Set a new screen drawing
		img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
		draw = ImageDraw.Draw(img)

		#Message to display and position
		w, h = font.getsize(todaysDateOutput)
		x = (inky_display.WIDTH / 2) - (w / 2)
		y = (inky_display.HEIGHT / 8) - (h / 8)

		#Draw the text on the screen
		draw.text((x, y), todaysDateOutput, inky_display.RED, font)
		draw.text((x, 40), binOneOutput, inky_display.BLACK, fontInfo)
		draw.text((x, 60), binTwoOutput, inky_display.BLACK, fontInfo)
		draw.text((x, 85), lastUpdatedString, inky_display.BLACK, fontUpdated)
		inky_display.set_image(img)
		inky_display.show()

	except:
		print ("Error outputing bin details")



#Main
def main():
	try:
		print ("Main method")
		theurl="YOUR_LOCAL_COUNCILS_SITE"
		pullBinPage(theurl)

		
	except:
		print ("Error with main")
    

if __name__ == "__main__":
    main()