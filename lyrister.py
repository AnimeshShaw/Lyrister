#!/usr/bin/env python
import requests
import sys
import os
from bs4 import BeautifulSoup

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
If song exists then you will be prompted for the directory where you want
to save the file and the filename with which you want to save the lyrics.

All files will be saved in .txt format and hence don't specify the extension
along with the filename.
'''


class Lyrister:
    def __init__(self, song, dir, filename):
        self.song = str(song)
        self.dir = str(dir)
        self.filename = str(filename)

    def processRequest(self):

        fileSavePath = self.dir + self.filename + '.txt'
        if os.path.exists(fileSavePath):
            print("Invalid Directory Path or File already exits.\n"
                  "Please Choose another name or check the path "
                  "you entered.\nProgram Exitting.")
            sys.exit(1)

        if not os.access(self.dir, os.W_OK):
            print("\nYou don't have the permission to create a file in this directory.\n"
                  "Choose another directory write permission. Program Quitting")
            sys.exit(1)

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

            with open(fileSavePath, 'w+') as f:
                f.write(lyrics[0].text)
            print("\n\nSong Name : %s" % self.song)
            print("\nSaved in Directory : %s" % self.dir)
            print("\nSong Lyrics Saved as  : %s.txt" % self.filename)
        else:
            print('Sorry we couldn\'t get the lyrics of the requested song!')


def printHeaders():
    print(Title)
    print(Description)


def getDetails():
    song = raw_input("\nEnter name of the Song : ")
    dir = raw_input("\nEnter Directory Path where you want to save the file (should end with trailing slash) : ")
    filename = raw_input("\nEnter name of the file : ")
    return song, dir, filename


def Usage():
    print("Usage : python Lyrister.py <name-of-song> <directory-location> <filename>\n"
          "If you don't understand these then just do the following : \n"
          "python Lyrister.py\n\nThe rest of the instructions will follow.\n"
          "Note: If your song name contains space then write the song name within double \nquotes"
          "else you will get argument error.")


if __name__ == "__main__":
    if len(sys.argv) == 1:
        printHeaders()
        song, dir, filename = getDetails()
        lyrister = Lyrister(song, dir, filename)
        lyrister.processRequest()
    elif len(sys.argv) == 4:
        printHeaders()
        song = sys.argv[1]
        dir = sys.argv[2]
        filename = sys.argv[3]
        lyrister = Lyrister(song, dir, filename)
        lyrister.processRequest()
    else:
        sys.stderr.write("Incorrect number of Arguments.\n\n")
        Usage()
