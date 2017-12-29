This set of scripts is designed to be used with the following spreadsheets from Softconf/START:
* a spreadsheet showing bids by reviewers
* a spreadsheet showing Toronto Paper Matching System scores for reviewers
In both cases, the spreadsheet will be contain one submission per line, and the format should be csv.
Sample bid and TPMS files are included and usage is demonstrated on them as follows:
find reviewers with no "yes" bids
% python findNoBidders.py --bidsFile bidsFile.csv
% python findNoBidders.py -bf bidsFile.csv
print, for each submission, the bid and TPMS score for the top n reviewers
% python giveMeReviewers.py --bidsFile bidsFile.csv --tpmsFile tpmsFile.csv
print bids/scores for one submission
% python giveMeReviewers.py --bf bidsFile.csv --tf tpmsFile.csv -p 100
 print bids/scores sorted by scores, rather than bids
% python giveMeReviewers.py -bf bidsFile.csv -tf tpmsFile.csv -p 100 -t
