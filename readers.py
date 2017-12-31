import csv
import re

# this function is necessary because START uses different ways to refer to reviewers in different spreadsheets
def fixUpNames(listOfNamesIds):
	return [re.sub(r'\s*\([^\)]+\)\s*', '', x) for x in listOfNamesIds]

def makeNamesIdsMapping(listOfNamesIds, namesIds):
	for nameId in listOfNamesIds:
		try:
			name, id = nameId.split('(', 2)
			id = id.strip()	
			id = id.rstrip(')')
			name = name.strip()
			namesIds[name] = id
		except:
			pass

# reads in the assignments csv; there should be one row per reviewer, NOT one row per submission
def readAssignments(assignmentsFile):
	assignments = {}
	if assignmentsFile != "":
		with open(assignmentsFile, encoding='utf-8', errors='ignore') as csvfile:
			assignmentsReader = csv.reader(csvfile)
			header = next(assignmentsReader)
			for row in assignmentsReader:
				assignments[row[0] + " " + row[1]] = len(row[2:])-1
	return assignments

# reads in the TPMS csv; there should be one row per submission, NOT one row per reviewer
def readTPMS(tpmsFile):
	tpms = {}
	namesIds = {}
	if tpmsFile != "":
		with open(tpmsFile, encoding='utf-8', errors='ignore') as csvfile:
			tpmsReader = csv.reader(csvfile)
			header = next(tpmsReader)
			for row in tpmsReader:
				makeNamesIdsMapping(row[1::2], namesIds)
				tpms[row[0]] = dict(zip(fixUpNames(row[1::2]), row[2::2]))
	return tpms, namesIds

# finds bidders who entered "yes" bids 
def findYesBidders(bids):
	bidders = {}
	for paper in bids:
		for bidder in bids[paper]:
			if bids[paper][bidder] == '1':
				bidders[bidder] = 1
	return bidders

# reads in the bids CSV, one row per paper with bidders along the columns
def readBids(bidsFile):
	bids = {}
	if bidsFile != "":
		with open(bidsFile, encoding='utf-8', errors='ignore') as csvfile:
			bidsReader = csv.reader(csvfile)
			header = next(bidsReader)
			for row in bidsReader:
				bids[row[0]] = dict(zip(header[1:], row[1:]))
	return bids

# reads in the quotas CSV, one row per reviewer
def readQuotas(quotasFile):
	quotas = {}
	if quotasFile != "":
		with open(quotasFile, encoding='utf-8', errors='ignore') as csvfile:
			quotasReader = csv.reader(csvfile)
			header = next(quotasReader)
			for row in quotasReader:
				quotas[row[0]] = row[-1]
	return quotas
