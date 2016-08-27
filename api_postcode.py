#!/usr/bin/env python
import os
import csv, json
from bottle import run, get, route, request, response


csvfile = r'/home/krishna/python_assignment/data/postcodes.csv'
counter = 1
last_nine_postcodes = []
all_ten_postcodes = []

def lookup_csv(lookupcsvfile, postcode_request, request_count):
	current_postcode = dict()
	global last_nine_postcodes
	global all_ten_postcodes
	with open(lookupcsvfile, 'rt') as f:
		reader = csv.reader(f, delimiter=',')
		for row in reader:
			if row[0] == postcode_request:
				current_postcode = {
					'Altitude': row[26],
					'Built up area': row[21],
					'Built_up_subdivision': row[22],
					'Constituency': row[14],
					'Country': row[12],
					'County': row[7],
					'CountyCode': row[13],
					'District': row[8],
					'DistrictCode': row[10],
					'Easting': row[4],
					'GridRef': row[6],
					'Households': row[20],
					'In use?': row[1],
					'Introduced': row[15],
					'Latitude': row[2],
					'Longitude': row[3],
					'Lower layer super output area': row[23],
					'National_park': row[18],
					'Northing': row[5],
					'Parish': row[17],
					'Population': row[19],
					'Postcode': row[0],
					'Region': row[25],
					'Rural/urban': row[24],
					'Terminated': row[16],
					'Ward': row[9],
					'WardCode': row[11],
					}
				if request_count % 10 == 1:
					last_nine_postcodes = []
					last_nine_postcodes.insert(0, current_postcode)
				elif 2 <= request_count % 10 <= 9:
					last_nine_postcodes.insert(0, current_postcode)
				if request_count % 10 == 0:
					all_ten_postcodes = [current_postcode, last_nine_postcodes]
					return all_ten_postcodes
				else:
					return current_postcode
@route('/geocode')
def bottle_lookup_csv():
	response.content_type = 'application/json'
	count = int( request.cookies.get('counter', '0') )
	count += 1
	response.set_cookie('counter', str(count))
	print (count)
	postcode_specified = request.GET.get('postcode', '').strip()
	result = lookup_csv(csvfile, postcode_specified, count)
	result = json.dumps(result, sort_keys=True, indent=4, separators=(', ', ': '))
	return result
	
					
if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))
	run(host='0.0.0.0', port=port, debug=True)