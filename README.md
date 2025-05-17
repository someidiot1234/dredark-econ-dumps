# shipsgz-reader
MD5: 0eb114325e7e7de1a7103e1ea21332b3\
SHA256: 0eecbe0741ee9e73c47f591512a1c49ff57da14f727110f14ba8bcebf57c308c\
Downloads the shipsgz file at inputted date and returns the information of a specified hex code.
if not working, make sure that the days and months inputted have no leading zeros.

# shipsgz-compressor
MD5: 9687db76128aebb1975a6e04e773caad\
SHA256: 8ec6d0850db3ddacbd0ecf2341d84abacfbade2ab1a3104a0d2fb5405f9f407c\
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
MD5: 6d7d02d2138f89f2d264f162b7f6e3a3\
SHA256: faa534e7b8d002b023a8e36163491813c7b055d22f75ce9457919b4dc4f5a0ac\
Downloading and Compressing https://pub.drednot.io/econ/prod/DAY_MONTH_YEAR/summary.json\
PLEASE specify the date range you would like to download on lines 170 & 171\

# summary reader
MD5: 0edae08638862e3530a8e0c52e157b9f\
SHA256: 70a46c9225aa8a1ea25dac0ec3408c76239729eff73960a3fbf8fba9810e3c57\
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
MD5: b960dc16d45fb0029173acc8246e441b\
SHA256: 2b609263d0513751580ce2c86dbe9446c9d7a7b589be8e43f7a04c604ca06855\
A folder that contains all summary files from November 23rd 2022 to May 10th 2025\
\
Have fun!\
