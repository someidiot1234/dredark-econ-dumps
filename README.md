# shipsgz-reader
Downloads the shipsgz file at inputted date and returns the information of a specified hex code.
if not working, make sure that the days and months inputted have no leading zeros.

# shipsgz-compressor
Compressing and Decompressing https://pub.drednot.io/econ/prod/DAY_MONTH_YEAR/ships.json.gz\
input filename, compressed filename, output filename are NOT specified.\
filename function I made:\
def getfilename(url):\
    # gets the index of "econ" in the url\
    info = url.index("econ")\
    unformatted = (url[(info)+5:])[:-5]\
    # removes the econ part and the link before it\
    # formats name to use underscore instead of slash\
    unformatted = unformatted.replace("_", "-")\
    formatted = unformatted.replace("/", "_") + ".bin"\
    return formatted\
# summary downloader/compressor
Downloading and Compressing https://pub.drednot.io/econ/prod/DAY_MONTH_YEAR/summary.json\
PLEASE specify the date range you would like to download on lines 170 & 171\
# summary reader
Decompresses the files made by the summary compressor.\
Takes input as filename in terminal. Saves output as json.\
Schema:\
total_ships - 15 bit integer\
total_logs - 31 bit integer\
items_held - an object that stores all new items created during that day.\ 
     Maps id (9 bit integer stored as string) to count (63 bit integer)\
items_grabbed - same as items_held\
items_new - an object that stores zone, source, and id:[total, grabbed]\
     "Zone":{"Bot":{"id":[total,grabbed]}}\
     id is a 9 bit integer, total/grabbed are 31 bit integers\
# summary files
A folder that contains all summary files from November 23rd 2022 to May 10th 2025\
\
Have fun!\
