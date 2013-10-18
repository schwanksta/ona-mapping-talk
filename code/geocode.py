import csv
import time
from googlegeocoder import GoogleGeocoder

geocoder = GoogleGeocoder()

with open("/Users/kschwen/Dev/personal/ona-mapping-talk/project/data/raw_inspections.csv", "r") as f:
    data = list(csv.reader(f))

with open("/Users/kschwen/Dev/personal/ona-mapping-talk/project/data/geocoded_inspections.csv", "w") as f:
    writer = csv.writer(f)
    for row in data:
        # Full address are the 3 columns after the first.
        full_address = "%s, %s, CA, %s" % (row[1], row[2], row[3])
        try:
            search = geocoder.get(full_address)
            row.append(search[0].geometry.location.lat)
            row.append(search[0].geometry.location.lng)
            print row
            writer.writerow(row)
            time.sleep(.5)
        except:
            print "Couldn't geocode ", row
