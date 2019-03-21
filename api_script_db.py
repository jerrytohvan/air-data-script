#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests,json,sys,time,psycopg2
from os import environ
from importlib import reload
from flask import Flask


reload(sys)
#sys.setdefaultencoding("utf-8")

start_str_request ="https://api.waqi.info/feed/" 
end_str_request = "/?token=1131b4b44f7cc5c89854245f4f65e2110ba27a5d"




cities1=["indonesia/jakarta/us-consulate/central","indonesia/jakarta/us-consulate/south",
"singapore/east","singapore/south","singapore/central","singapore/north","singapore/west","vietnam/ho-chi-minh-city/us-consulate", "vietnam/da-nang","thailand/koh-chang-sub-district-health-promoting-hospital-maesai", "thailand/chiangrai---gaia-station-05","thailand/chiangrai---gaia-station-06","thailand/chiangrai---gaia-station-02","thailand/chiangrai---gaia-station-01","thailand/chiangrai---gaia-station-07","thailand/chiang-rai-hospital",
"thailand/chiangrai/maesai-health-office","thailand/chiangrai---gaia-station-03","thailand/chiangrai/natural-resources-and-environment-office","thailand/fang-hospital","thailand/chai-prakan-hospital","thailand/muang-na-sub-district-municipality","thailand/nan/a.-nanoi","thailand/phrao-hospital","thailand/chiangmai/phrao-gaia04",
"thailand/chiang-dao-public-heath-office", "thailand/mae-taeng-hospital","thailand/arunothai-sub-district-health-promoting-hospital","thailand/wiang-haeng-hospital","thailand/mae-hong-son/pai-hospital","thailand/pang-ma-pha-hospital","thailand/mae-hong-son/srisangwan-hospital","thailand/mae-hongson/natural-resources-and-environment-office","thailand/mae-hong-son/hongsonsuksa-school","thailand/khun-yuam-hospital",
"thailand/mae-sa-sub-district-health-promoting-hospital","thailand/mae-hae-nuea-sub-district-health-promoting-hospital","thailand/debaratana-hospital","thailand/kong-khaek-sub-district-administrative-organization","thailand/chom-tong-hospital","thailand/mae-wang-hospital","thailand/chiangmai/maerim---prem","thailand/cnx/t.-mae-ram","thailand/nakornping-hospital",
"thailand/chiangmai/city-hall","thailand/rihes-cmu","thailand/lee-la-noodle/cmru","thailand/chiangmai---cmis","thailand/true-regional-office","thailand/hpc-1","thailand/ban-thammapakorn","thailand/chiang-mai/yupparaj-wittayalai-school","thailand/hpc-1","thailand/chiang-mai/ltd./aia-co.","thailand/true-regional-office","thailand/cnx/t.-pa-dad/iv","thailand/cnx/cmu-mae-hia","thailand/san-kamphaeng-hospital","thailand/sarapee-hospital"]

cities2=["thailand/hang-dong-hospital","thailand/mae-wang-hospital","thailand/chom-tong-hospital","thailand/hod-hospital","thailand/mae-hong-son/mae-sariang-hospital","thailand/mae-hong-son/sop-moei-hospital","thailand/omkoi-hospital","thailand/mae-on-hospital","thailand/lamphun/suanboonyopatham","thailand/lamphun/provincial-administrative-stadium","thailand/phayao/knowledge-park","thailand/phayao/pong-hospital","thailand/nan/municipality-office","thailand/nan/chaloem-phra-kiat/huai-kon","thailand/phrae/song-hospital","thailand/phrae-meteorological-station","thailand/phrae/rong-kwang-hospital",
	 "thailand/phrae/long-hospital","thailand/lampang/health-promotion-hospital-sob-pad","thailand/lampang/provincial-waterworks-authority-mae-moh","thailand/lampang-meteorological-station","thailand/sam-ngao-hospital",
"thailand/tak/mae-sot/mae-pa","thailand/loei/provincial-health-office","thailand/khonkaen","thailand/nakhon-ratchasima/municipal-waste-water-pumping-station","thailand/sa-kaeo/aranyaprathed/sriaranyothai-kindergarten","thailand/nakhon-sawan/nakhonsawan-irrigation","thailand/kanchanaburi/kanchanaburi/pak-prak","thailand/regional-environmental-office-8","thailand/ayutthaya/ayutthaya-witthayalai-school","thailand/nonthaburi/sukhothai-thammathirat-open-university","thailand/bangkok/national-housing-authority-klongchan",
"thailand/bangkok/bodindecha-sing-singhaseni-school","thailand/bangkok/chokchai-police-station","thailand/bangkok/national-housing-authority-huaykwang","thailand/bangkok/national-housing-authority-dindaeng","thailand/the-thailand-research-fund-trf","thailand/rama-iv-expressway-fes","thailand/bangkok/chulalongkorn-hospital","thailand/bangkok/thonburi-power-sub-station","thailand/bangkok/bansomdejchaopraya-rajabhat-university","thailand/samut-prakan/prabadang-rehabiltation-center","thailand/samut-prakan/residence-for-dept.-of-primary-industries-and-mines",
"thailand/samut-prakan/city-hall","thailand/bangkok/thai-meteorological-department-bangna","thailand/bangkok/ratburana-post-office","thailand/bangkok/thai-meteorological-department-bangna","thailand/samut-prakan/national-housing-authority-bangplee","thailand/chonburi/general-education-office","thailand/chachoengsao/wang-yen-subdistrict-administrative","thailand/chonburi/health-promotion-hospital-ban-khao-hin","thailand/saraburi/khao-noi-fire-station","thailand/chonburi/laem-chabang-municipal-stadium","thailand/pluakdaeng-district-health-office","thailand/rayong/field-crop-research-center",
"thailand/nakhon-ratchasima/municipal-waste-water-pumping-station","thailand/mobile-8","thailand/rayong/agricultural-office","thailand/rayong/government-center"]

def launch():
	print("launching script...")
	# with open('output.csv', 'a') as f:
	try:
		connection = psycopg2.connect(user="eksmcidgmnrgma", password="fe2c2308d89d9f66ac2efcf1e5eebac8363d4d112e006a985523a3960bfb18ad", host="ec2-50-17-227-28.compute-1.amazonaws.com", port="5432", database="d96iof88teppel")
		cursor = connection.cursor()
		postgres_insert_query = """ INSERT INTO air_data (city,lon,lat,pm25,pm10,so2,o3,co,datetimestamp) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
		for r in cities2:
			query = requests.get(start_str_request+r+end_str_request)
			json_data = json.loads(query.text)

			if 'geo' in json_data['data']['city']:
				lon = str(json_data['data']['city']['geo'][0]).strip()
				lat = str(json_data['data']['city']['geo'][1]).strip()
			else: 
				lon = ''
				lat = ''

			if 'city' in json_data['data']:
				city = str(json_data['data']['city']).strip()
			else:
				city = ''

			if 'time' in json_data['data']:
				time = str(json_data['data']['time']['s']).strip()
			else:
				time = ''

			city = json_data['data']['city']['name']

			if 'pm25' in json_data['data']['iaqi']:
				pm25 = str(json_data['data']['iaqi']['pm25']['v']).strip()
			else:
				pm25 = ''

			if 'pm10' in json_data['data']['iaqi']:
				pm10 = str(json_data['data']['iaqi']['pm10']['v']).strip()
			else:
				pm10 = ''

			if 'so2' in json_data['data']['iaqi']:
				so2 = str(json_data['data']['iaqi']['so2']['v']).strip()
			else:
				so2 = ''

			if 'o3' in json_data['data']['iaqi']:
				o3 = str(json_data['data']['iaqi']['o3']['v']).strip()
			else:
				o3 = ''

			if 'co' in json_data['data']['iaqi']:
				co = str(json_data['data']['iaqi']['co']['v']).strip()
			else:
				co = ''

			# csv_w.writerow([city,lon,lat,pm25, pm10, so2, o3, co,time])
			record_to_insert = (city,lon,lat,pm25, pm10, so2, o3, co,time)
			cursor.execute(postgres_insert_query, record_to_insert)
			connection.commit()
			#print (r)
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

