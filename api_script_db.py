

import requests,json,sys,time,psycopg2
from os import environ
from importlib import reload
from flask import Flask

#reload(sys)
sys.setdefaultencoding('utf8')

start_str_request ="https://api.waqi.info/feed/" 
end_str_request = "/?token=1131b4b44f7cc5c89854245f4f65e2110ba27a5d"

cities=["indonesia/jakarta/us-consulate/central","indonesia/jakarta/us-consulate/south","indonesia/palembang", "indonesia/jabungtimur", "indonesia/pontianak","indonesia/batam","indonesia/pekanbaru","indonesia/medan", "indonesia/palangkaraya", "indonesia/buntok", "indonesia/muarateweh", 
 "singapore","singapore/east","singapore/south","singapore/central","singapore/north","singapore/west","vietnam/ho-chi-minh-city/us-consulate", "vietnam/da-nang"]



def launch():
	print("launching script...")
	# with open('output.csv', 'a') as f:
	try:
		connection = psycopg2.connect(user="eksmcidgmnrgma", password="fe2c2308d89d9f66ac2efcf1e5eebac8363d4d112e006a985523a3960bfb18ad", host="ec2-50-17-227-28.compute-1.amazonaws.com", port="5432", database="d96iof88teppel")
		cursor = connection.cursor()
		postgres_insert_query = """ INSERT INTO air_data (city,lon,lat,pm25,pm10,so2,o3,co,datetimestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		for r in cities:
			query = requests.get(start_str_request+r+end_str_request)
			json_data = json.loads(query.text)

			if 'geo' in json_data['data']['city']:
				lon = str(json_data['data']['city']['geo'][0]).encode('utf-8').strip()
				lat = str(json_data['data']['city']['geo'][1]).encode('utf-8').strip()
			else: 
				lon = ''
				lat = ''

			if 'city' in json_data['data']:
				city = str(json_data['data']['city']).encode('utf-8').strip()
			else:
				city = ''

			if 'time' in json_data['data']:
				time = str(json_data['data']['time']['s']).encode('utf-8').strip()
			else:
				time = ''

			city = json_data['data']['city']['name']

			if 'pm25' in json_data['data']['iaqi']:
				pm25 = str(json_data['data']['iaqi']['pm25']['v']).encode('utf-8').strip()
			else:
				pm25 = ''

			if 'pm10' in json_data['data']['iaqi']:
				pm10 = str(json_data['data']['iaqi']['pm10']['v']).encode('utf-8').strip()
			else:
				pm10 = ''

			if 'so2' in json_data['data']['iaqi']:
				so2 = str(json_data['data']['iaqi']['so2']['v']).encode('utf-8').strip()
			else:
				so2 = ''

			if 'o3' in json_data['data']['iaqi']:
				o3 = str(json_data['data']['iaqi']['o3']['v']).encode('utf-8').strip()
			else:
				o3 = ''

			if 'co' in json_data['data']['iaqi']:
				co = str(json_data['data']['iaqi']['co']['v']).encode('utf-8').strip()
			else:
				co = ''

			# csv_w.writerow([city,lon,lat,pm25, pm10, so2, o3, co,time])
			record_to_insert = (city,lon,lat,pm25, pm10, so2, o3, co,time)
			cursor.execute(postgres_insert_query, record_to_insert)
			connection.commit()
			count = cursor.rowcount
			print (count, "Record inserted successfully into air_data table")
	except (Exception, psycopg2.Error) as error :
	    if(connection):
	        print("Failed to insert record into mobile table", error)
	        
	finally:
	    #closing database connection.
	    if(connection):
	        cursor.close()
	        connection.close()
	        print("PostgreSQL connection is closed")

	# csv_w = csv.writer(f)
	# csv_w.writerow(" ")
	
	print("writting done...")




while(True):
	launch()
	print("script sleeping...")
	time.sleep(60*60)




app = Flask(__name__)
app.run(environ.get('PORT'))

