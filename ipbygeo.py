#!/usr/bin/env python
# -*- coding: utf-8 -*-
from update import *
from tools import *
import argparse
from math import sqrt
import sys
import os

output_kml_ = ""
output_txt_ = ""

logo = bcolors.OKGREEN+bcolors.BOLD+"""  _____       ____         _____            
 |_   _|     |  _ \       / ____|           
   | |  _ __ | |_) |_   _| |  __  ___  ___  
   | | | '_ \|  _ <| | | | | |_ |/ _ \/ _ \ 
  _| |_| |_) | |_) | |_| | |__| |  __/ (_) |
 |_____| .__/|____/ \__, |\_____|\___|\___/ 
       | |           __/ |                  
       |_|          |___/  """+bcolors.FAIL+"""by Zion3R        
                        www.blackploit.com"""+bcolors.OKGREEN+"""  
IpByGeo: Find ip by geographic range"""+bcolors.ENDC

arg_parser = argparse.ArgumentParser(description=logo+'''
	
	Example invocation:
	# NBC
	python ipbygeo.py -l 40.758943 -73.979356 -r 0.005 
	Long:
	python ipbygeo.py --location 40.758943 -73.979356 --radius 0.005 --output_kml NBC.kml --output_txt NBC.txt --target "NBC Studios"
	python ipbygeo.py --l 40.758943 -73.979356 --r 0.005 --ok NBC.kml --ot NBC.txt --t "NBC Studios"
	# White House
	python ipbygeo.py --location 38.897676 -77.03653 --radius 0.005
	python ipbygeo.py --location 34.211264 116.600546 --radius 0.005


''', formatter_class=argparse.RawTextHelpFormatter)

arg_parser.add_argument('--update', '-u', required=False, help="Update Database http://dev.maxmind.com/geoip/", action="store_true")
arg_parser.add_argument('--input_ipv4', '-i4', required=False, help='CSV file to read data Ipv4', default="./data/GeoLite2-City-Blocks-IPv4.csv")
arg_parser.add_argument('--input_ipv6', '-i6', required=False, help='CSV file to read data Ipv6', default="./data/GeoLite2-City-Blocks-IPv6.csv")
arg_parser.add_argument('--output_dir', '-d', required=False, type=str, help='Output dir for resulting files',default ="./output")
arg_parser.add_argument('--output_kml', '-ok', required=False, help='KML file to write data and read with Google Earth')
arg_parser.add_argument('--output_txt', '-ot', required=False, help='TXT file to write networks found')
arg_parser.add_argument('--delimiter', required=False, type=str, help="Delimiter from input file", default=",")
arg_parser.add_argument('--location','-l', required=False, nargs=2, type=float, metavar=('LAT', 'LON'), help='Geolocation coordinates')
arg_parser.add_argument('--radius','-r', required=False, type=float, help='Radius in degrees, 1 degree = 111.12 km aprox', default=0.005)
arg_parser.add_argument('--target', '-t', required=False, help='Target name', default="TARGET")
args = arg_parser.parse_args()

def main():
	testWritePermissions()
	if not os.path.isfile(FILE_DB_CSV):
		colorMessage("process","Database downloading ...")
		updateDB()
		okey()

	elif args.update:
		colorMessage("process","Database updating ...")
		updateDB()
		okey()
		sys.exit()

	if args.location != None and args.radius != None:
		setOutputFiles()
		print logo+"\n"

		addHeaderKML(args.location, args.radius)
		addTargetKML()
		# Ipv4
		print "\t"*4+bcolors.OKBLUE+bcolors.BOLD+"[ Ipv4 ]"+bcolors.ENDC
		Ipv4NetworkLatLong = finder(csvToArr(args.input_ipv4, args.delimiter), "Ipv4")
		colorMessage("process", "Writing KML file: "+str(args.output_dir+"/"+output_kml_))
		colorMessage("process", "Writing TXT file: "+str(args.output_dir+"/"+output_txt_))
		for i in Ipv4NetworkLatLong:
			addPointKML(i[0],i[1], i[2])
			writeTXT(i[0],"a+")
		# Ipv6
		print "\n"+"\t"*4+bcolors.OKBLUE+bcolors.BOLD+"[ Ipv6 ]"+bcolors.ENDC
		Ipv6NetworkLatLong = finder(csvToArr(args.input_ipv6, args.delimiter), "Ipv6")
		colorMessage("process", "Writing KML file: "+str(args.output_dir+"/"+output_kml_))
		colorMessage("process", "Writing TXT file: "+str(args.output_dir+"/"+output_txt_))
		for i in Ipv6NetworkLatLong:
			addPointKML(i[0],i[1], i[2])
			writeTXT(i[0],"a+")

		addFooterKML()
		colorMessage("info", "Done!")
		colorMessage("info2", args.output_dir+"/"+output_kml_, "Output KML file (open with Google Earth)")
		colorMessage("info2", args.output_dir+"/"+output_txt_, "Output TXT file (IP address list)")
	else:
		if args.update:
			sys.exit()
		colorMessage("fail", "--location / --radius parameters are necesary")
		colorMessage("warning", "Run for help: python ipbygeo.py --help")


def finder(arrNetworkLatLong, comment = ""):
	colorMessage("process", "Finding Ip address "+str(comment))
	arr = []
	for i in arrNetworkLatLong:
		try:
			network = i[0]
			latitude = float(i[1])
			longitude = float(i[2])
			if distanceToCenter(latitude, longitude) < args.radius:
				arr.append([network, latitude, longitude])
		except Exception, e:
			continue
	colorMessage("info2", str(len(arr)), "networks found! "+str(comment))
	okey()
	return arr

def distanceToCenter(latitude, longitude):
	centerLatitude = args.location[0]
	centerLongitude = args.location[1]
	return sqrt((centerLatitude-latitude)**2 + (centerLongitude-longitude)**2)

def addHeaderKML(centerPoint, radius):
	textHeader = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n\t<Document>\n\t\t<name>IP Location for "+str(args.target)+" "+str(centerPoint)+" and radius "+str(radius)+"°</name>\n\t\t<description>IP Location for "+str(centerPoint)+" and radius "+str(radius)+"°</description>\n\t\t<Style id=\"targetPlacemark\">\n\t\t\t<IconStyle>\n\t\t\t\t<Icon>\n\t\t\t\t\t<href>http://maps.google.com/mapfiles/kml/pal3/icon28.png</href>\n\t\t\t\t</Icon>\n\t\t\t</IconStyle>\n\t\t</Style>\n\t\t<atom:link rel=\"related\" href=\"http://www.blackploit.com\" />\n\t\t<Folder>"
	writeKML(textHeader, 'w+')

def addTargetKML():
	textPoint = "\t\t\t<Placemark>\n\t\t\t\t<name>TARGET "+str(args.location)+"</name>\n\t\t\t\t<styleUrl>#targetPlacemark</styleUrl>\n\t\t\t\t<Point>\n\t\t\t\t\t<coordinates>"+str(args.location[1])+","+str(args.location[0])+",0</coordinates>\n\t\t\t\t</Point>\n\t\t\t</Placemark>"
	writeKML(textPoint, 'a')

def addPointKML(network, latitude, longitude):
	textPoint = "\t\t\t<Placemark>\n\t\t\t\t<name>"+str(network)+"</name>\n\t\t\t\t<Point>\n\t\t\t\t\t<coordinates>"+str(longitude)+","+str(latitude)+",0</coordinates>\n\t\t\t\t</Point>\n\t\t\t</Placemark>"
	writeKML(textPoint, 'a')

def addFooterKML():
	textFooter = "\t\t</Folder>\n\t</Document>\n</kml>"
	writeKML(textFooter, 'a')
	okey()

def writeKML(text, option):
	try:
		with open(args.output_dir+"/"+output_kml_, option) as myfile:
			myfile.write(text+"\n")
	except Exception, e:
		colorMessage("fail", "sudo permissions required! "+str(e))
		sys.exit()

def writeTXT(text, option):
	try:
		with open(args.output_dir+"/"+output_txt_, option) as myfile:
			myfile.write(text+"\n")
	except Exception, e:
		colorMessage("fail", "sudo permissions required! "+str(e))
		sys.exit()

def testWritePermissions():
	global output_txt_
	try:
		if not os.path.exists(DATA_FOLDER):
			os.makedirs(DATA_FOLDER)

		if not os.path.exists(args.output_dir):
			os.makedirs(args.output_dir)
		with open(args.output_dir+"/"+output_txt_, "w") as myfile:
			myfile.write("\n")
	except Exception, e:
		colorMessage("fail", "sudo permissions required! "+str(e))
		sys.exit()

def setOutputFiles():
	global output_kml_
	global output_txt_
	if args.output_kml == None:
		output_kml_ = "lat"+str(args.location[0])+"lon"+str(args.location[1])+"rad"+str(args.radius)+".kml"
	else:
		output_kml_ = args.output_kml
	if args.output_txt == None:
		output_txt_ = "lat"+str(args.location[0])+"lon"+str(args.location[1])+"rad"+str(args.radius)+".txt"
	else:
		output_txt_ = args.output_txt

if __name__ == '__main__':
	main()