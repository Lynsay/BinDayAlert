# 🗑 Bin Day Alert ♻️

[![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/)  ![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/Lynsay/BinDayAlert)  ![GitHub last commit](https://img.shields.io/github/last-commit/Lynsay/BinDayAlert)  [![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

Script to grab the date of the next bin collection from the Local Council's website.

## Description
This script requests the HTML of the Local Council's webpage.  XPath expressions are then used to navigate the DOM, returning information relating to the dates various bins will be emptied (e.g. refuse, recycling, food, etc.).  This information is then written to an Inky pHAT e-paper display from [Pimoroni](https://github.com/pimoroni), attached to a Raspberry Pi Zero W.  It is suggested the script is run regularly as a cron job (once per day).

<img src="BinDayAlert.jpg" alt="Bin Day Alert" title="Bin Day Alert" width="300" height="300" />

## Requirements
To run the script, the following packages are required:

* `Pillow` - Python Imaging Library (Fork) Pillow
* `inky` - Python library for the [Pimoroni](https://github.com/pimoroni) Inky pHAT e-paper display
* `lxml` - Used to parse the DOM of the webpage
* `requests` - Requests the HTML of a webpage
* `nexmo` - SMS service

Install these via pip:

`pip install Pillow inky lxml requests nexmo`

## 🔨To complete
- Tidy script
