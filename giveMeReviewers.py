import argparse
import csv
import itertools
import re
import sys

# this function is necessary because START uses different ways to refer to reviewers in different spreadsheets
def fixUpNames(listOfNamesIds):
	return [re.sub(r'\s*\([^\)]+\)\s*', '', x) for x in listOfNamesIds]

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
	if tpmsFile != "":
		with open(tpmsFile, encoding='utf-8', errors='ignore') as csvfile:
			tpmsReader = csv.reader(csvfile)
			header = next(tpmsReader)
			for row in tpmsReader:
				tpms[row[0]] = dict(zip(fixUpNames(row[1::2]), row[2::2]))
	return tpms

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

# prints for one or more submissions bid and TPMS score info sorted by TPMS score
def printByTPMS(bids, tpms, yesbidders, assignments, papers):
	for paper in papers:
		for reviewer in sorted(tpms[paper], key=tpms[paper].get, reverse=True):
			score = tpms[paper][reviewer]
			bid = bids[paper][reviewer] if paper in bids and reviewer in bids[paper] and reviewer in yesbidders else "nb"
			assignment = assignments[reviewer] if len(assignments) > 0 and reviewer in assignments else "0" if len(assignments) > 0 else ""
			if score != "na" or bid != "nb":
				print(paper, "\t", reviewer, "\t", tpms[paper][reviewer], "\t", bid, "\t", assignment)

# prints for one or more submissions bid and TPMS score info sorted by bid
def printByBids(bids, tpms, yesbidders, assignments, papers):
	for paper in papers:
		for reviewer in sorted(bids[paper], key=bids[paper].get):
			score = tpms[paper][reviewer] if paper in tpms and reviewer in tpms[paper] else "na"
			bid = bids[paper][reviewer] if reviewer in yesbidders else "nb"
			assignment = assignments[reviewer] if len(assignments) > 0 and reviewer in assignments else "0" if len(assignments) > 0 else ""
			if score != "na" or bid != "nb":
				print(paper, "\t", reviewer, "\t", bid, "\t", score, "\t", assignment)

# initializes argument parser
def setUpParser():
	parser = argparse.ArgumentParser(description='Print reviewers by bids or TPMS scores.')
	parser.add_argument('--bidsFile', '-bf', default="", help='a csv file containing bids per submission')
	parser.add_argument('--tpmsFile', '-tf', default="", help='a csv file containing TPMS scores per submission')
	parser.add_argument('--assignmentsFile', '-af', default="", help='a csv file containing submission assignments per reviewer')
	parser.add_argument('--papers', '-p', nargs='+', default=[], help='list of papers for which to print out results')
	parser.add_argument('--byTPMS', '-t', action='store_true', help='print results in order of TPMS scores (default: print results in order of bids)')
	return parser

args = setUpParser().parse_args()
bids = readBids(args.bidsFile)
yesbidders = findYesBidders(bids)
tpms = readTPMS(args.tpmsFile)
assignments = readAssignments(args.assignmentsFile)
if args.byTPMS == True:
	papers = tpms.keys() if len(args.papers) == 0 else args.papers
	printByTPMS(bids, tpms, yesbidders, assignments, papers)
else:
	papers = bids.keys() if len(args.papers) == 0 else args.papers
	printByBids(bids, tpms, yesbidders, assignments, papers)


