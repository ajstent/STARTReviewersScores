import argparse
import sys

import readers

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
bids = readers.readBids(args.bidsFile)
yesbidders = readers.findYesBidders(bids)
tpms = readers.readTPMS(args.tpmsFile)
assignments = readers.readAssignments(args.assignmentsFile)
if args.byTPMS == True:
	papers = tpms.keys() if len(args.papers) == 0 else args.papers
	printByTPMS(bids, tpms, yesbidders, assignments, papers)
else:
	papers = bids.keys() if len(args.papers) == 0 else args.papers
	printByBids(bids, tpms, yesbidders, assignments, papers)


