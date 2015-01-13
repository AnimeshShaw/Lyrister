#!/usr/bin/env python
import requests, sys, os
from argparse import ArgumentParser

__author__ = "Psycho_Coder <psychocoder@outlook.com>"
__date__ = "May 14, 2014"

Title = '''
  _            _    _
 | |  _  _ _ _(_)__| |_ ___ _ _
 | |_| || | '_| (_-<  _/ -_) '_|
 |____\_, |_| |_/__/\__\___|_|
	  |__/

			  By Psycho_Coder
				Version : 1.0
		'''

Description = '''
Enter the Song name for which you want to get the lyrics and press return.
Lyrics will be printed to stdout.
Minor tweaks by github.com/d4rkcat.
'''


class Lyrister:
	def __init__(self, song):
		self.song = str(song)

	def processRequest(self):
		req = requests.get("http://www.google.com/search?q=" + self.song.replace(' ', '+') + '+lyrics')
		encodedQuery = req.text.encode('ascii', 'ignore')
		req.close()

		soup = BeautifulSoup(encodedQuery)
		songLink = ''
		elemAttr = soup.select("h3 a")

		for link in elemAttr:
			if str(link.attrs["href"]).find('azlyrics') > 0:
				songLink = str(link.attrs["href"])
				songLink = songLink[songLink.find('http'):(songLink.find('html') + len('html'))]
				break

		if songLink:
			req = requests.get(songLink)
			encodedQuery = req.text.encode('ascii', 'ignore')
			req.close()

			soup = BeautifulSoup(encodedQuery)
			lyrics = soup.findAll('div', {'style': 'margin-left:10px;margin-right:10px;'})

			print(lyrics[0])
		else:
			print('Sorry we couldn\'t get the lyrics of the requested song!')


if __name__ == "__main__":
	try:
		from bs4 import BeautifulSoup
	except ImportError:
		print("To execute this app. You need BeautifulSoup4 library. Please Read Helpdocs on how to install the "
			  "library")
		exit(0)

	if not sys.stdin.isatty():
		for line in sys.stdin:
			lyrister = Lyrister(line)
			lyrister.processRequest()
	else:
		parser = ArgumentParser(prog='lyrister', usage='./lyrister.py [options] (-h for help)')
		parser.add_argument('-s', "--song", type=str, help='Song name to search lyrics for.', required = True)
		args = parser.parse_args()

		lyrister = Lyrister(args.song)
		lyrister.processRequest()
