This set of scripts is designed to be used with the following spreadsheets from Softconf/START:
* a spreadsheet showing bids by reviewers
* a spreadsheet showing Toronto Paper Matching System scores for reviewers

In both cases, the spreadsheet will be contain one submission per line, and the format should be csv.
Sample bid and TPMS files are included and usage is demonstrated on them as follows:

* find reviewers with no "yes" bids

% python findNoBidders.py --bidsFile bidsFile.csv

% python findNoBidders.py -bf bidsFile.csv

* print, for each submission, the bid and TPMS score for the top n reviewers

% python giveMeReviewers.py --bidsFile bidsFile.csv --tpmsFile tpmsFile.csv

* print bids/scores for one submission, paper number 100

% python giveMeReviewers.py --bf bidsFile.csv --tf tpmsFile.csv -p 100

-----

100      Kit Kat         1       0.9602699

100      Johann Thoms    2       1

100      Wei Guo         2       0.979992

100      Sally Smith     3       0.9276914

100      Anju Patel      4       0.9484952

-----

* print bids/scores sorted by scores, rather than bids

% python giveMeReviewers.py -bf bidsFile.csv -tf tpmsFile.csv -p 100 -t

-----

100      Johann Thoms    1       2

100      Wei Guo         0.979992        2

100      Kit Kat         0.9602699       1

100      Anju Patel      0.9484952       4

100      Sally Smith     0.9276914       3

100      Mog Roll        0.9133105       nb

-----

* add assignment information (for your track) so you know how "loaded" reviewers are:

% python giveMeReviewers.py -bf bidsFile.csv -tf tpmsFile.csv -af assignmentsFile.csv -p 100 -t 