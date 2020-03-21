import re
import sys
import csv
import json
from unidecode import unidecode

# Custom function to correctly capitalize the words 
def upperPart(name):
  keep = [
    "tbc",
    "c.f.r"
  ]
  if name.isupper() and name.lower() in keep:
    return name
  if name.isupper() and not (name.lower() in keep):
    return name.capitalize()
  
  toUpper = [
    "general"
  ]
  if name in toUpper:
    return name.capitalize()
  return name

# Get rid of unusable information about the minister
def cleanMinisters(name):
  ministers = [
    "Ministerul Apararii Nationale",
    "Ministerul Administratiei si Internelor",
    "Ministerul Transporturilor si Infrastructurii",
    "Ministerul Justitiei - Administratia Nationala a Penitenciarelor Penitenciar"
  ]
  for minister in ministers:
    name = name.replace(minister, "")
  return name

# Parse all hospitals
def parseAll():
  with open("hospitals.csv", "r") as csvfile:
    with open("final.txt", "r") as final:
      hospitals = []
      csvreader = csv.reader(csvfile)
      next(csvreader)
      
      for row in csvreader:
        # Consider only the name from the current row
        name = row[4]
        finalLine = final.readline()
        
        # Take the values of the coordinates
        pos1 = finalLine.find("(")
        pos2 = finalLine[pos1:].find(")")
        coords = finalLine[(pos1 + 1) : (pos1 + pos2)].split(",")
        latitude = float(coords[0])
        longitude = float(coords[1])
        
        # Get rid of the minister information
        name = cleanMinisters(name).strip()
        
        # And correctly capitalize each word
        saved = []
        parts = name.split()
        finalName = ""
        for index, part in enumerate(parts):
          part = upperPart(part)
          if index == len(parts) - 1:
            finalName += part
          else:
            finalName += part
            finalName += " "
        # Optional: get rid of diacritics
        hospitalName = unidecode(finalName)
        
        # And add the new hospital
        hospitals.append({
          'name' : hospitalName,
          'latitude' : latitude,
          'longitude' : longitude,
          'beds' : 0,
          'respirators' : 0
        })
      return hospitals
    
def main():
  # Dump to json file
  with open('json_data.txt', 'w') as file:
    hospitals = parseAll()
    json.dump(hospitals, file)
  
if __name__ == '__main__':
  main()
