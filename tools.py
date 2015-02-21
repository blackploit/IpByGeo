#!/usr/bin/env python
# -*- coding: utf-8 -*-

import platform
import numpy as np
import csv

class bcolors:
	if platform.system() == "Linux":
		HEADER = '\033[95m'
		OKBLUE = '\033[94m'
		OKGREEN = '\033[92m'
		WARNING = '\033[93m'
		FAIL = '\033[91m'
		ENDC = '\033[0m'
		BOLD = '\033[1m'
		UNDERLINE = '\033[4m'
	else:
		HEADER = ''
		OKBLUE = ''
		OKGREEN = ''
		WARNING = ''
		FAIL = ''
		ENDC = ''
		BOLD = ''
		UNDERLINE = ''

		#print bcolors.FAIL+bcolors.BOLD+"[ ! ] --location / --radius parameters are necesary"+bcolors.ENDC
		#print bcolors.WARNING+bcolors.BOLD+"[ * ] Run for help: python ipbygeo.py --help"+bcolors.ENDC

def colorMessage(typeMessage, text, secondText = ""):
	if typeMessage == "process":
		print bcolors.OKBLUE+bcolors.BOLD+"[ * ] "+bcolors.ENDC+bcolors.BOLD+str(text)+bcolors.ENDC
	elif typeMessage == "fail":
		print bcolors.FAIL+bcolors.BOLD+"[ ! ] "+bcolors.ENDC+bcolors.BOLD+str(text)+bcolors.ENDC
	elif typeMessage == "warning":
		print bcolors.WARNING+bcolors.BOLD+"[ - ] "+bcolors.ENDC+bcolors.BOLD+str(text)+bcolors.ENDC
	elif typeMessage == "info":
		print bcolors.OKGREEN+bcolors.BOLD+"[ i ] "+bcolors.ENDC+bcolors.BOLD+str(text)+bcolors.ENDC
	elif typeMessage == "info2":
		print bcolors.OKGREEN+bcolors.BOLD+"[ i ] "+bcolors.ENDC+bcolors.FAIL+bcolors.BOLD+str(text)+" "+bcolors.ENDC+bcolors.BOLD+str(secondText)+bcolors.ENDC
	else:
		print text

def csvToArr(filename,delimiter_):
	colorMessage("process", "Reading CSV file: "+str(filename))
	arrAux = []
	networkLatLong =[]
	try:
		data = csv.reader(open(filename, 'rU'),delimiter=delimiter_)
		for row in data:
			arrAux.append(row)
		del data
		arrAux = np.delete(arrAux, (0), axis=0) # del first row
		arrAux = np.array(arrAux).transpose()
		networkLatLong.append(arrAux[0]) # Network
		networkLatLong.append(arrAux[7]) # Latitude
		networkLatLong.append(arrAux[8]) # Longitude
	except IOError as e:
		colorMessage("fail", "error! Input file not found\n"+str(e))
		return []
	except Exception as e:
		colorMessage("fail", "error! Unexpected error while reading input file \n"+str(e))
		return []
	del arrAux
	okey()
	return np.array(networkLatLong).transpose()

def okey():
	print "\t"*8+bcolors.OKGREEN+bcolors.BOLD+"[ OK ]"+bcolors.ENDC