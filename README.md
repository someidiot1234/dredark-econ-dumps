# shipsgz-compressor
Compressing and Decompressing https://pub.drednot.io/econ/prod/DAY_MONTH_YEAR/ships.json.gz
input filename, compressed filename, output filename are NOT specified.
filename function I made:
def getfilename(url):
    # gets the index of "econ" in the url
    info = url.index("econ")
    unformatted = (url[(info)+5:])[:-5]
    # removes the econ part and the link before it
    # formats name to use underscore instead of slash
    unformatted = unformatted.replace("_", "-")
    formatted = unformatted.replace("/", "_") + ".bin"
    return formatted

Have fun!
