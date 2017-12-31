import argparse
import sys

import readers

def getQuota(namesIds, quotas, reviewer):
	if reviewer in namesIds and namesIds[reviewer] in quotas:
		return quotas[namesIds[reviewer]]
	else:
		return "3"

# prints for one or more submissions bid and TPMS score info sorted by TPMS score
def printByTPMS(bids, tpms, yesbidders, namesIds, quotas, assignments, papers):
	for paper in papers:
		if paper in tpms:
			for reviewer in sorted(tpms[paper], key=tpms[paper].get, reverse=True):
				score = tpms[paper][reviewer]
				bid = bids[paper][reviewer] if paper in bids and reviewer in bids[paper] and reviewer in yesbidders else "nb"
				quota = getQuota(namesIds, quotas, reviewer)
				assignment = assignments[reviewer] if len(assignments) > 0 and reviewer in assignments else "0" if len(assignments) > 0 else ""
				if score != "na" or bid != "nb":
					print(paper, "\t", reviewer, "\t", tpms[paper][reviewer], "\t", bid, "\t", assignment)
		else:
			print("No paper id " + paper + " in tpms scores")

# prints for one or more submissions bid and TPMS score info sorted by bid
def printByBids(bids, tpms, yesbidders, namesIds, quotas, assignments, papers):
	for paper in papers:
		if paper in bids:
			for reviewer in sorted(bids[paper], key=bids[paper].get):
				score = tpms[paper][reviewer] if paper in tpms and reviewer in tpms[paper] else "na"
				bid = bids[paper][reviewer] if reviewer in yesbidders else "nb"
				quota = getQuota(quotas, namesIds, reviewer)
				assignment = assignments[reviewer] if len(assignments) > 0 and reviewer in assignments else "0" if len(assignments) > 0 else ""
				if score != "na" or bid != "nb":
					print(paper, "\t", reviewer, "\t", bid, "\t", score, "\t", assignment)
		else:
			print("No paper id " + paper + " in bids")

# initializes argument parser
def setUpParser():
	parser = argparse.ArgumentParser(description='Print reviewers by bids or TPMS scores.')
	parser.add_argument('--bidsFile', '-bf', default="", help='a csv file containing bids per submission')
	parser.add_argument('--tpmsFile', '-tf', default="", help='a csv file containing TPMS scores per submission')
	parser.add_argument('--quotasFile', '-qf', default="", help='a csv file containing quotas per reviewer')
	parser.add_argument('--assignmentsFile', '-af', default="", help='a csv file containing submission assignments per reviewer')
	parser.add_argument('--papers', '-p', nargs='+', default=[], help='list of papers for which to print out results')
	parser.add_argument('--byTPMS', '-t', action='store_true', help='print results in order of TPMS scores (default: print results in order of bids)')
	return parser

args = setUpParser().parse_args()
bids = readers.readBids(args.bidsFile)
yesbidders = readers.findYesBidders(bids)
tpms, namesIds = readers.readTPMS(args.tpmsFile)
quotas = readers.readQuotas(args.quotasFile)
assignments = readers.readAssignments(args.assignmentsFile)
if args.byTPMS == True:
	papers = tpms.keys() if len(args.papers) == 0 else args.papers
	printByTPMS(bids, tpms, yesbidders, namesIds, quotas, assignments, papers)
else:
	papers = bids.keys() if len(args.papers) == 0 else args.papers
	printByBids(bids, tpms, yesbidders, namesIds, quotas, assignments, papers)


