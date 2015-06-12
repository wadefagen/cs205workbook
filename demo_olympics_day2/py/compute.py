import csv
import json
    
def do_compute():
  file = open('res/olympicAthletes.csv')
  reader = csv.DictReader(file)
  
  countries = {}
  
  for row in reader:
    country = row['Country']
    medals = int(row['Gold Medals'])
  
    if country in countries:
      countries[country] += medals
    else:
      countries[country] = medals
      
  # Write out JSON to file 
  f = open('res/goldMedals.json', 'w')
  s = json.dumps(countries, indent = 4, ensure_ascii = False)
  f.write(s)