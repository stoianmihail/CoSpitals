import re
import sys
import csv
import html
import string
import urllib.request
from unidecode import unidecode

def getHtmlText(url):
# get the html text from this url
  # Connect to the site
  request = urllib.request.Request(url)
  response = urllib.request.urlopen(request)
    
  # Decode the site into utf-8
  return response.read().decode('utf-8')

def parseGPS(hospital):
  pattern = "https://www.google.com/maps/search/"
  text = getHtmlText(pattern + hospital)
  gpsPattern = "center="
  pos = text.find(gpsPattern)
  nextPos = text[pos:].find('&')
  gps = text[(pos + len(gpsPattern)):(pos + nextPos)]
  splitted = gps.split("%2C")
  if len(splitted) < 2:
    print("error: " + hospital)
    sys.exit(1)
    pass
  else:
    latitude = splitted[0]
    longitude = splitted[1]
  return (latitude, longitude)

def parseAll(fileName):
  with open(fileName, "r") as csvfile:
    csvreader = csv.reader(csvfile)
    fields = next(csvreader)
    print(fields)
    
    output = open("saved.txt", "w")
    
    hospitals = []
    for row in csvreader:
      if int(row[0]) <= 44:
        continue
      name = row[4]
      name = name.replace(" ", "+")
      name = re.sub('[^a-zA-Z+]+', '', name)
      coord = parseGPS(name)
      print(name + " -> " + str(coord))
      output.write(name + str(coord) + "\n")
      hospitals.append((name, coord)) 
    output.close()
    return hospitals

def main(fileName):
  hospitals = parseAll(fileName)
  print(hospitals)
  pass
  
if __name__ == '__main__':
  main(sys.argv[1])
