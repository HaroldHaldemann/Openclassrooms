#include:utf-8

import sys
import os
try:
	import bs4
except ModuleNotFoundError:
	print("BS4 module is not installed, " \
		"please report to README.md for further informations"
	)
	sys.exit()
import requests
import re
import urllib.request
import main

def replace_multiple_caracters(string, caracters, replacement):
	"""
	Take a string you want to replace, 
	a string of caracters you want to replace
	and the caracter of replacement of these caracters
	Replace the caracters by their replacement.
	"""
	for caracter in caracters:
		string = string.replace(caracter, replacement)
	return string

def acquire_html(url):
	"""
	Take a url.
	Return the BeautifulSoup content of this url.
	"""
	try:
		response = requests.get(url)
		soup = bs4.BeautifulSoup(response.content, 'lxml')
	except requests.exceptions.ConnectionError:
		print("Cannot reach the site, " \
			"please check your internet connection"
		)
		sys.exit()
	except bs4.FeatureNotFound:
		print("lxml parser library is not installed, " \
			"please report to README.md for further informations."
		)
		sys.exit()
	return soup

def acquire_title(soup):
	"""
	Take a BeautifulSoup content of a book page.
	Return the title of the book.
	"""
	title = soup.h1.string
	return title

def acquire_code_tax_number(soup):
	"""
	Take a BeautifulSoup content of a book page.
	Return the code, the price with and without tax 
	and the number available of the book.
	"""
	table = soup.table.find_all('td')
	code_tax_number = {
		'universal_product_code': table[0].string,
		'price_including_tax': table[3].string,
		'price_excluding_tax': table[2].string,
		'number_available': table[5].string,
	}
	return code_tax_number

def acquire_category(soup):
	"""
	Take a BeautifulSoup content of a book page.
	Return the category of the book.
	"""
	table = soup.ul.find_all('a')
	category = table[2].string
	return category

def acquire_star_rating(soup):
	"""
	Take a BeautifulSoup content of a book page.
	Return the rating of the book.
	"""
	review_rating = soup.find(
		class_=re.compile("^star")
	)['class'][1]
	return review_rating

def acquire_image_url(soup):
	"""
	Take a BeautifulSoup content of a book page.
	Return the url of the image of the book.
	"""
	partial_url = soup.img['src'][5:]
	image_url = f"http://books.toscrape.com{partial_url}"
	return image_url

def acquire_image_path(soup):
	"""
	Take a BeautifulSoup content of a book page.
	Download the image of the book.
	Return the absolute path to the images.
	"""
	category = f"{acquire_category(soup)}".replace(" ","")
	title = f"{acquire_title(soup)}"
	title = replace_multiple_caracters(title, ",;.*?!'\" ", "")
	title = replace_multiple_caracters(title, ":/\\|<>", "-")
	if not os.path.exists(f"{main.path}BookImages/{category}"):
		os.mkdir(f"{main.path}BookImages/{category}")
	urllib.request.urlretrieve(
		acquire_image_url(soup),
		f"{main.path}BookImages/{category}/{title}.jpg",
	)
	path = f"{main.path}BookImages/{category}/{title}.jpg"
	return path

def acquire_product_description(soup):
	"""
	Take a BeautifulSoup content of a book page.
	Return the description of the book.
	"""
	is_description =  soup.find('p', {'class': None})
	if is_description:
		product_description = is_description.string
	else:
		product_description = ""
	return product_description

def info_book(url):
	"""
	Take a url of a book page.
	Return a list of the informations of a book.
	Download the image of the book.
	"""
	soup = acquire_html(url)
	return [
		url,
		acquire_code_tax_number(soup)['universal_product_code'],
		acquire_title(soup),
		acquire_code_tax_number(soup)['price_including_tax'],
		acquire_code_tax_number(soup)['price_excluding_tax'],
		acquire_code_tax_number(soup)['number_available'],
		acquire_category(soup),
		acquire_star_rating(soup),
		acquire_image_url(soup),
		acquire_image_path(soup),
		acquire_product_description(soup),
	]

