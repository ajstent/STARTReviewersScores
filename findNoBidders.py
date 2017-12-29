import argparse
import csv
import itertools
import re
import sys

# finds bidders who entered no "yes" bids 
def findNoBidders(bids):
	bidders = {}
	yesbidders = {}
	for paper in bids:
		for bidder in bids[paper]:
			bidders[bidder] = 1
			if bids[paper][bidder] == '1':
				yesbidders[bidder] = 1
	return set(bidders.keys()) - set(yesbidders.keys())

# reads in the bids CSV, one row per paper with bidders along the columns
def readBids(bidsFile):
	bids = {}
	with open(bidsFile, encoding='utf-8', errors='ignore') as csvfile:
		bidsReader = csv.reader(csvfile)
		header = next(bidsReader)
		for row in bidsReader:
			bids[row[0]] = dict(zip(header[1:], row[1:]))
	return bids

# initializes argument parser
def setUpParser():
	parser = argparse.ArgumentParser(description='Print reviewers by bids or TPMS scores.')
	parser.add_argument('--bidsFile', '-bf', default='bids.csv', help='a csv file containing bids per submission')
	return parser

args = setUpParser().parse_args()
bids = readBids(args.bidsFile)
nobidders = findNoBidders(bids)
with open("nobidders.txt", "w", encoding='utf-8', errors='ignore') as outFile:
	for nobidder in sorted(nobidders):
		outFile.write(nobidder + '\n')
