#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib2
import zipfile
import hashlib
from tools import colorMessage

FILE_DB_CSV = "GeoLite2-City-CSV.zip"
DATA_FOLDER = "./data"

def updateDB():
	if isUpToDate():
		colorMessage("info","Database is Up-to-date")
		extractZipDB()
	else:
		downloadDB()
		extractZipDB()

def isUpToDate():
	colorMessage("process","Checking md5 checksum")
	try:
		localChecsum = str(hashlib.md5(open(FILE_DB_CSV).read()).hexdigest())
		urlChecksun = "http://geolite.maxmind.com/download/geoip/database/"+FILE_DB_CSV+".md5"
		onlineChecksum = str(urllib2.urlopen(urlChecksun).read())
		if localChecsum == onlineChecksum:
			return True
		else:
			return False
	except Exception, e:
		return False

def downloadDB():
	url = "http://geolite.maxmind.com/download/geoip/database/"+FILE_DB_CSV
	file_name = url.split('/')[-1]
	u = urllib2.urlopen(url)
	f = open(file_name, 'wb')
	meta = u.info()
	file_size = int(meta.getheaders("Content-Length")[0])
	colorMessage("process","Downloading: %s Bytes: %s" % (file_name, file_size))
	file_size_dl = 0
	block_sz = 8192
	while True:
	    buffer = u.read(block_sz)
	    if not buffer:
	        break
	    file_size_dl += len(buffer)
	    f.write(buffer)
	    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
	    status = status + chr(8)*(len(status)+1)
	    print status,
	f.close()

def extractZipDB():
	colorMessage("process","Extracting "+FILE_DB_CSV)
	zfile = zipfile.ZipFile(FILE_DB_CSV)
	# Ipv4
	folderName = str(zfile.namelist()[0]).split("/")[0]
	dataIpv4 = zfile.read(folderName+"/GeoLite2-City-Blocks-IPv4.csv", DATA_FOLDER)
	ipv4File = open(DATA_FOLDER+"/GeoLite2-City-Blocks-IPv4.csv", "w+")
	ipv4File.write(dataIpv4)
	ipv4File.close()
	# Ipv6
	dataIpv4 = zfile.read(folderName+"/GeoLite2-City-Blocks-IPv6.csv", DATA_FOLDER)
	ipv4File = open(DATA_FOLDER+"/GeoLite2-City-Blocks-IPv6.csv", "w+")
	ipv4File.write(dataIpv4)
	ipv4File.close()